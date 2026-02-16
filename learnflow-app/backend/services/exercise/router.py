"""
Exercise Service Router

Endpoints for exercise generation and grading.
"""

import time
from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

import structlog
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/exercise/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client, publish_event, get_state, save_state
from shared.models import HealthResponse
from shared.models.exercise import Difficulty, TestResult
from shared.models.events import ExerciseCompletedEvent, ProgressUpdatedEvent, StruggleDetectedEvent
from shared.models.struggle import StruggleType

from agent import generate_exercise, ExerciseSpec
from grader import grade_submission, GradeResult

router = APIRouter()
logger = structlog.get_logger(__name__)

# Track exercise start times for stuck detection
exercise_start_times: dict[str, datetime] = {}


class ExerciseGenerateResponse(BaseModel):
    """Response with generated exercise."""
    exercise_id: UUID
    title: str
    description: str
    starter_code: str
    expected_output_hint: Optional[str] = None


class ExerciseSubmitRequest(BaseModel):
    """Request for exercise submission."""
    student_id: UUID
    exercise_id: UUID
    code: str


class ExerciseSubmitResponse(BaseModel):
    """Response from exercise grading."""
    passed: bool
    score: float = Field(ge=0, le=1)
    test_results: list[TestResult]
    feedback: str
    time_spent_seconds: int


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="exercise",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.get("/exercises/generate", response_model=ExerciseGenerateResponse)
async def generate_coding_exercise(
    student_id: UUID = Query(..., description="Student ID"),
    topic: str = Query(..., description="Topic for the exercise"),
    difficulty: Optional[str] = Query(None, description="Difficulty level"),
) -> ExerciseGenerateResponse:
    """
    Generate a coding exercise based on topic and difficulty.

    Difficulty is determined by:
    1. Explicit difficulty parameter
    2. Student's mastery level for the topic
    3. Default to beginner
    """
    logger.info(
        "Generating exercise",
        student_id=str(student_id),
        topic=topic,
        difficulty=difficulty,
    )

    # Determine difficulty
    if not difficulty:
        # Get from student's mastery (simplified)
        difficulty = "beginner"

    diff_enum = Difficulty(difficulty.lower())

    # Generate exercise using AI
    exercise = await generate_exercise(
        topic=topic,
        difficulty=diff_enum,
    )

    # Store exercise for grading
    exercise_key = f"exercise:{exercise.exercise_id}"
    await save_state(exercise_key, exercise.model_dump(mode="json"))

    # Track start time for stuck detection
    start_key = f"start:{student_id}:{exercise.exercise_id}"
    exercise_start_times[start_key] = datetime.utcnow()

    return ExerciseGenerateResponse(
        exercise_id=exercise.exercise_id,
        title=exercise.title,
        description=exercise.description,
        starter_code=exercise.starter_code,
        expected_output_hint=exercise.expected_output_hint,
    )


@router.post("/exercises/grade", response_model=ExerciseSubmitResponse)
@router.post("/exercises/submit", response_model=ExerciseSubmitResponse)
async def submit_exercise(request: ExerciseSubmitRequest) -> ExerciseSubmitResponse:
    """
    Submit an exercise solution for grading.

    1. Retrieves exercise definition
    2. Runs code against test cases
    3. Calculates score and provides feedback
    4. Publishes completion event
    """
    logger.info(
        "Grading submission",
        student_id=str(request.student_id),
        exercise_id=str(request.exercise_id),
    )

    # Get exercise definition
    exercise_key = f"exercise:{request.exercise_id}"
    exercise_data = await get_state(exercise_key)

    if not exercise_data:
        raise HTTPException(status_code=404, detail="Exercise not found")

    # Calculate time spent
    start_key = f"start:{request.student_id}:{request.exercise_id}"
    start_time = exercise_start_times.get(start_key, datetime.utcnow())
    time_spent = int((datetime.utcnow() - start_time).total_seconds())

    # Check for stuck (>10 minutes)
    if time_spent > settings.struggle_stuck_minutes * 60:
        await _publish_stuck_alert(
            student_id=request.student_id,
            exercise_id=request.exercise_id,
            time_spent=time_spent,
        )

    # Grade the submission
    grade_result = await grade_submission(
        code=request.code,
        test_cases=exercise_data.get("test_cases", []),
    )

    # Generate feedback
    feedback = _generate_feedback(grade_result, exercise_data.get("topic_id", ""))

    # Publish completion event
    await publish_event(
        topic="exercise.completed",
        data=ExerciseCompletedEvent(
            source_service="exercise",
            student_id=request.student_id,
            exercise_id=request.exercise_id,
            topic_id=exercise_data.get("topic_id", "unknown"),
            passed=grade_result.passed,
            score=grade_result.score,
            time_spent_seconds=time_spent,
        ),
    )

    # Cleanup start time
    if start_key in exercise_start_times:
        del exercise_start_times[start_key]

    return ExerciseSubmitResponse(
        passed=grade_result.passed,
        score=grade_result.score,
        test_results=grade_result.test_results,
        feedback=feedback,
        time_spent_seconds=time_spent,
    )


@router.get("/exercises/topics")
async def get_exercise_topics() -> dict[str, list[str]]:
    """Get available exercise topics by difficulty."""
    return {
        "beginner": [
            "variables", "strings", "numbers", "lists basics",
            "if statements", "simple loops",
        ],
        "learning": [
            "functions", "list comprehensions", "dictionaries",
            "file handling", "error handling",
        ],
        "proficient": [
            "classes", "inheritance", "decorators",
            "generators", "context managers",
        ],
        "mastered": [
            "metaclasses", "async programming", "design patterns",
            "algorithms", "data structures",
        ],
    }


def _generate_feedback(result: GradeResult, topic: str) -> str:
    """Generate feedback based on grading result."""
    if result.passed:
        if result.score == 1.0:
            return "Excellent! All tests passed. Great job!"
        else:
            return f"Good work! You passed with a score of {result.score:.0%}. Review the failed tests to improve."
    else:
        failed_count = sum(1 for t in result.test_results if not t.passed)
        return f"{failed_count} test(s) failed. Review your code and try again. Focus on edge cases."


async def _publish_stuck_alert(
    student_id: UUID,
    exercise_id: UUID,
    time_spent: int,
) -> None:
    """Publish a struggle alert for stuck student."""
    await publish_event(
        topic=settings.topic_struggle_detected,
        data=StruggleDetectedEvent(
            source_service="exercise",
            student_id=student_id,
            struggle_type=StruggleType.STUCK,
            details={
                "exercise_id": str(exercise_id),
                "time_spent_seconds": time_spent,
                "threshold_minutes": settings.struggle_stuck_minutes,
            },
            confidence=min(0.5 + (time_spent / 600) * 0.3, 0.9),
        ),
    )
    logger.warning(
        "Stuck alert published",
        student_id=str(student_id),
        exercise_id=str(exercise_id),
        time_spent=time_spent,
    )
