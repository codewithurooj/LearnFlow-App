"""
Progress Service Event Handlers

Handles events from exercise and quiz completion for mastery updates.
"""

from datetime import datetime, date
from typing import Any, Optional
from uuid import UUID

import structlog

import sys
sys.path.insert(0, str(__file__).replace("services/progress/events.py", ""))

from shared.config import settings
from shared.dapr import get_state, save_state, publish_event
from shared.models.progress import MasteryScore
from shared.models.events import (
    ExerciseCompletedEvent,
    QuizCompletedEvent,
    ProgressUpdatedEvent,
    StruggleDetectedEvent,
)
from shared.models.struggle import StruggleType

from calculator import (
    update_mastery_score,
    create_initial_mastery,
    get_level_from_score,
    detect_milestones,
)
from models import StudentProgressState


logger = structlog.get_logger(__name__)


# Topic name mapping (in production, this would come from a database)
TOPIC_NAMES = {
    "variables": "Variables and Data Types",
    "strings": "String Operations",
    "lists": "Lists and Arrays",
    "dictionaries": "Dictionaries",
    "functions": "Functions",
    "loops": "Loops and Iteration",
    "conditionals": "Conditional Statements",
    "classes": "Classes and Objects",
    "exceptions": "Exception Handling",
    "file_io": "File Input/Output",
    "modules": "Modules and Packages",
    "decorators": "Decorators",
    "generators": "Generators and Iterators",
    "async": "Async Programming",
}


def get_topic_name(topic_id: str) -> str:
    """Get human-readable topic name."""
    return TOPIC_NAMES.get(topic_id, topic_id.replace("_", " ").title())


async def get_student_progress(student_id: UUID) -> StudentProgressState:
    """
    Get or create student progress state from Dapr state store.

    Args:
        student_id: The student's UUID

    Returns:
        StudentProgressState with all topic mastery data
    """
    state_key = f"progress:{student_id}"
    data = await get_state(state_key)

    if data:
        return StudentProgressState.model_validate(data)

    # Create new progress state
    new_state = StudentProgressState(
        student_id=student_id,
        topics={},
        current_streak=0,
    )
    await save_state(state_key, new_state.model_dump(mode="json"))
    return new_state


async def save_student_progress(state: StudentProgressState) -> bool:
    """
    Save student progress state to Dapr state store.

    Args:
        state: The progress state to save

    Returns:
        True if saved successfully
    """
    state_key = f"progress:{state.student_id}"
    state.updated_at = datetime.utcnow()
    return await save_state(state_key, state.model_dump(mode="json"))


def update_streak(state: StudentProgressState) -> int:
    """
    Update the streak count based on last activity date.

    Args:
        state: Current progress state

    Returns:
        Updated streak count
    """
    today = date.today().isoformat()
    last_date = state.last_activity_date

    if last_date is None:
        # First activity
        return 1

    if last_date == today:
        # Same day, no change
        return state.current_streak

    # Check if yesterday
    yesterday = (date.today() - __import__("datetime").timedelta(days=1)).isoformat()
    if last_date == yesterday:
        return state.current_streak + 1

    # Streak broken
    return 1


async def handle_exercise_completed(event: ExerciseCompletedEvent) -> dict[str, Any]:
    """
    Handle exercise completion event and update mastery.

    Args:
        event: The exercise completed event

    Returns:
        Result summary with old/new scores
    """
    logger.info(
        "Processing exercise completion",
        student_id=str(event.student_id),
        exercise_id=str(event.exercise_id),
        topic_id=event.topic_id,
        score=event.score,
    )

    # Get current progress state
    state = await get_student_progress(event.student_id)

    # Update streak
    new_streak = update_streak(state)
    state.current_streak = new_streak
    state.last_activity_date = date.today().isoformat()

    # Get or create topic mastery
    topic_data = state.topics.get(event.topic_id)
    if topic_data:
        current_mastery = MasteryScore.model_validate(topic_data)
    else:
        current_mastery = create_initial_mastery(
            student_id=event.student_id,
            topic_id=event.topic_id,
            topic_name=get_topic_name(event.topic_id),
        )

    old_score = current_mastery.total_score
    old_level = current_mastery.level

    # Convert score from 0-1 to 0-100
    exercise_score = event.score * 100

    # Update mastery with new exercise score
    new_mastery = update_mastery_score(
        current=current_mastery,
        exercise_score=exercise_score,
        streak_days=new_streak,
    )

    new_score = new_mastery.total_score
    new_level = new_mastery.level
    level_changed = old_level != new_level

    # Save updated topic mastery
    state.topics[event.topic_id] = new_mastery.model_dump(mode="json")
    await save_student_progress(state)

    # Publish progress update event
    await publish_event(
        topic=settings.topic_progress_updated,
        data=ProgressUpdatedEvent(
            source_service="progress",
            student_id=event.student_id,
            topic_id=event.topic_id,
            old_score=old_score,
            new_score=new_score,
            old_level=old_level,
            new_level=new_level,
            level_changed=level_changed,
        ),
    )

    # Detect milestones
    milestones = detect_milestones(old_score, new_score, get_topic_name(event.topic_id))

    if milestones:
        logger.info(
            "Milestones achieved",
            student_id=str(event.student_id),
            milestones=[m["message"] for m in milestones],
        )

    logger.info(
        "Mastery updated from exercise",
        student_id=str(event.student_id),
        topic_id=event.topic_id,
        old_score=old_score,
        new_score=new_score,
        level_changed=level_changed,
    )

    return {
        "old_score": old_score,
        "new_score": new_score,
        "old_level": old_level,
        "new_level": new_level,
        "level_changed": level_changed,
        "milestones": milestones,
    }


async def handle_quiz_completed(event: QuizCompletedEvent) -> dict[str, Any]:
    """
    Handle quiz completion event and update mastery.

    Args:
        event: The quiz completed event

    Returns:
        Result summary with old/new scores
    """
    logger.info(
        "Processing quiz completion",
        student_id=str(event.student_id),
        quiz_id=str(event.quiz_id),
        topic_id=event.topic_id,
        score=event.score,
    )

    # Get current progress state
    state = await get_student_progress(event.student_id)

    # Update streak
    new_streak = update_streak(state)
    state.current_streak = new_streak
    state.last_activity_date = date.today().isoformat()

    # Get or create topic mastery
    topic_data = state.topics.get(event.topic_id)
    if topic_data:
        current_mastery = MasteryScore.model_validate(topic_data)
    else:
        current_mastery = create_initial_mastery(
            student_id=event.student_id,
            topic_id=event.topic_id,
            topic_name=get_topic_name(event.topic_id),
        )

    old_score = current_mastery.total_score
    old_level = current_mastery.level

    # Convert score from 0-1 to 0-100
    quiz_score = event.score * 100

    # Update mastery with new quiz score
    new_mastery = update_mastery_score(
        current=current_mastery,
        quiz_score=quiz_score,
        streak_days=new_streak,
    )

    new_score = new_mastery.total_score
    new_level = new_mastery.level
    level_changed = old_level != new_level

    # Save updated topic mastery
    state.topics[event.topic_id] = new_mastery.model_dump(mode="json")
    await save_student_progress(state)

    # Check for struggle (low quiz score)
    if quiz_score < settings.struggle_low_score_threshold * 100:
        await publish_event(
            topic=settings.topic_struggle_detected,
            data=StruggleDetectedEvent(
                source_service="progress",
                student_id=event.student_id,
                struggle_type=StruggleType.LOW_SCORE,
                topic_id=event.topic_id,
                details={
                    "quiz_id": str(event.quiz_id),
                    "score": quiz_score,
                    "threshold": settings.struggle_low_score_threshold * 100,
                    "questions_correct": event.questions_correct,
                    "questions_total": event.questions_total,
                },
                confidence=0.8,
            ),
        )
        logger.warning(
            "Low quiz score detected",
            student_id=str(event.student_id),
            score=quiz_score,
        )

    # Publish progress update event
    await publish_event(
        topic=settings.topic_progress_updated,
        data=ProgressUpdatedEvent(
            source_service="progress",
            student_id=event.student_id,
            topic_id=event.topic_id,
            old_score=old_score,
            new_score=new_score,
            old_level=old_level,
            new_level=new_level,
            level_changed=level_changed,
        ),
    )

    logger.info(
        "Mastery updated from quiz",
        student_id=str(event.student_id),
        topic_id=event.topic_id,
        old_score=old_score,
        new_score=new_score,
        level_changed=level_changed,
    )

    return {
        "old_score": old_score,
        "new_score": new_score,
        "old_level": old_level,
        "new_level": new_level,
        "level_changed": level_changed,
    }
