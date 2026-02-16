"""
Progress Service Router

Endpoints for student progress tracking and mastery retrieval.
"""

from datetime import datetime
from typing import Any
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException

import sys
sys.path.insert(0, str(__file__).replace("services/progress/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client
from shared.models import HealthResponse
from shared.models.progress import MasteryScore
from shared.models.events import ExerciseCompletedEvent, QuizCompletedEvent

from calculator import (
    calculate_overall_mastery,
    calculate_improvement_suggestions,
    get_level_from_score,
)
from events import (
    get_student_progress,
    handle_exercise_completed,
    handle_quiz_completed,
    get_topic_name,
)
from models import (
    ProgressSummaryResponse,
    TopicDetailResponse,
    TopicMasteryResponse,
    MasteryBreakdownResponse,
)


router = APIRouter()
logger = structlog.get_logger(__name__)


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for Kubernetes probes."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="progress",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.get("/progress/{student_id}", response_model=ProgressSummaryResponse)
async def get_progress_summary(student_id: UUID) -> ProgressSummaryResponse:
    """
    Get overall progress summary for a student.

    Returns mastery scores for all topics and overall statistics.
    """
    logger.info("Fetching progress summary", student_id=str(student_id))

    state = await get_student_progress(student_id)

    # Build topic summaries
    topic_summaries: list[TopicMasteryResponse] = []
    mastery_scores: list[MasteryScore] = []

    for topic_id, topic_data in state.topics.items():
        mastery = MasteryScore.model_validate(topic_data)
        mastery_scores.append(mastery)

        topic_summaries.append(
            TopicMasteryResponse(
                topic_id=topic_id,
                topic_name=mastery.topic_name,
                mastery_score=mastery.total_score,
                mastery_level=mastery.level,
                level_color=mastery.level_color,
            )
        )

    # Calculate overall mastery
    overall_mastery = calculate_overall_mastery(mastery_scores)
    overall_level = get_level_from_score(overall_mastery)

    # Calculate totals
    total_exercises = sum(m.exercises_completed for m in mastery_scores)
    total_quizzes = sum(m.quizzes_taken for m in mastery_scores)

    return ProgressSummaryResponse(
        student_id=student_id,
        overall_mastery=overall_mastery,
        overall_level=overall_level,
        topics=topic_summaries,
        current_streak=state.current_streak,
        last_activity=state.updated_at,
        total_exercises=total_exercises,
        total_quizzes=total_quizzes,
    )


@router.get("/progress/{student_id}/topic/{topic_id}", response_model=TopicDetailResponse)
async def get_topic_progress(student_id: UUID, topic_id: str) -> TopicDetailResponse:
    """
    Get detailed progress for a specific topic.

    Returns mastery breakdown with component scores and improvement suggestions.
    """
    logger.info(
        "Fetching topic progress",
        student_id=str(student_id),
        topic_id=topic_id,
    )

    state = await get_student_progress(student_id)

    topic_data = state.topics.get(topic_id)
    if not topic_data:
        raise HTTPException(
            status_code=404,
            detail=f"No progress found for topic '{topic_id}'",
        )

    mastery = MasteryScore.model_validate(topic_data)
    suggestions = calculate_improvement_suggestions(mastery)

    breakdown = MasteryBreakdownResponse(
        exercises_score=mastery.exercises_score,
        quizzes_score=mastery.quizzes_score,
        code_quality_score=mastery.code_quality_score,
        streak_bonus=mastery.streak_bonus,
        exercises_completed=mastery.exercises_completed,
        quizzes_taken=mastery.quizzes_taken,
    )

    return TopicDetailResponse(
        topic_id=topic_id,
        topic_name=mastery.topic_name,
        mastery_score=mastery.total_score,
        mastery_level=mastery.level,
        level_color=mastery.level_color,
        breakdown=breakdown,
        improvement_suggestions=suggestions,
        last_activity=mastery.last_activity,
    )


@router.get("/progress/{student_id}/topics")
async def list_student_topics(student_id: UUID) -> dict[str, list[TopicMasteryResponse]]:
    """
    Get list of all topics for a student with their mastery levels.

    Groups topics by mastery level for easy dashboard display.
    """
    logger.info("Listing student topics", student_id=str(student_id))

    state = await get_student_progress(student_id)

    by_level: dict[str, list[TopicMasteryResponse]] = {
        "Mastered": [],
        "Proficient": [],
        "Learning": [],
        "Beginner": [],
    }

    for topic_id, topic_data in state.topics.items():
        mastery = MasteryScore.model_validate(topic_data)
        response = TopicMasteryResponse(
            topic_id=topic_id,
            topic_name=mastery.topic_name,
            mastery_score=mastery.total_score,
            mastery_level=mastery.level,
            level_color=mastery.level_color,
        )
        by_level[mastery.level].append(response)

    return by_level


# Dapr pub/sub event handlers


@router.post("/events/exercise-completed")
async def handle_exercise_event(event: dict[str, Any]) -> dict[str, str]:
    """Handle exercise completion events from Dapr pub/sub."""
    try:
        data = event.get("data", {})
        exercise_event = ExerciseCompletedEvent.model_validate(data)

        result = await handle_exercise_completed(exercise_event)

        logger.info(
            "Processed exercise completion event",
            event_id=str(exercise_event.event_id),
            level_changed=result["level_changed"],
        )

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error("Failed to process exercise completion", error=str(e))
        return {"status": "DROP"}


@router.post("/events/quiz-completed")
async def handle_quiz_event(event: dict[str, Any]) -> dict[str, str]:
    """Handle quiz completion events from Dapr pub/sub."""
    try:
        data = event.get("data", {})
        quiz_event = QuizCompletedEvent.model_validate(data)

        result = await handle_quiz_completed(quiz_event)

        logger.info(
            "Processed quiz completion event",
            event_id=str(quiz_event.event_id),
            level_changed=result["level_changed"],
        )

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error("Failed to process quiz completion", error=str(e))
        return {"status": "DROP"}
