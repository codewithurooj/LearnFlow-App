"""
Mastery Calculator

Implements weighted mastery calculation with EMA smoothing.
Formula: exercises (40%) + quizzes (30%) + code quality (20%) + streak (10%)
"""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import structlog

import sys
sys.path.insert(0, str(__file__).replace("services/progress/calculator.py", ""))

from shared.config import settings
from shared.models.progress import MasteryScore


logger = structlog.get_logger(__name__)


def calculate_ema(
    new_value: float,
    current_ema: float,
    alpha: float = 0.3,
) -> float:
    """
    Calculate Exponential Moving Average.

    Args:
        new_value: The new value to incorporate
        current_ema: The current EMA value
        alpha: Smoothing factor (0-1), higher = more weight on recent values

    Returns:
        Updated EMA value
    """
    return alpha * new_value + (1 - alpha) * current_ema


def calculate_streak_bonus(consecutive_days: int) -> float:
    """
    Calculate streak bonus based on consecutive days of activity.

    Args:
        consecutive_days: Number of consecutive days with activity

    Returns:
        Streak bonus score (0-100)
    """
    # Each day adds 10 points, capped at 100
    return min(consecutive_days * 10, 100)


def calculate_exercise_score(
    scores: list[float],
    limit: int = 10,
) -> float:
    """
    Calculate exercise score using EMA of recent attempts.

    Args:
        scores: List of exercise scores (0-100), most recent last
        limit: Maximum number of recent scores to consider

    Returns:
        EMA-smoothed exercise score (0-100)
    """
    if not scores:
        return 0.0

    recent_scores = scores[-limit:]
    ema = recent_scores[0]

    for score in recent_scores[1:]:
        ema = calculate_ema(score, ema)

    return round(ema, 2)


def calculate_quiz_score(
    scores: list[float],
    limit: int = 5,
) -> float:
    """
    Calculate quiz score using average of recent quizzes.

    Args:
        scores: List of quiz scores (0-100)
        limit: Maximum number of recent quizzes to consider

    Returns:
        Average quiz score (0-100)
    """
    if not scores:
        return 0.0

    recent_scores = scores[-limit:]
    return round(sum(recent_scores) / len(recent_scores), 2)


def calculate_code_quality_score(
    ratings: list[float],
) -> float:
    """
    Calculate code quality score from code review ratings.

    Args:
        ratings: List of code quality ratings (0-100)

    Returns:
        Average code quality score (0-100)
    """
    if not ratings:
        return 50.0  # Default to neutral

    return round(sum(ratings) / len(ratings), 2)


def update_mastery_score(
    current: MasteryScore,
    exercise_score: Optional[float] = None,
    quiz_score: Optional[float] = None,
    code_quality: Optional[float] = None,
    streak_days: Optional[int] = None,
) -> MasteryScore:
    """
    Update a mastery score with new values using EMA smoothing.

    Args:
        current: Current mastery score
        exercise_score: New exercise score (if completing an exercise)
        quiz_score: New quiz score (if completing a quiz)
        code_quality: New code quality rating
        streak_days: Current streak in days

    Returns:
        Updated MasteryScore with recalculated values
    """
    new_exercises = current.exercises_score
    new_quizzes = current.quizzes_score
    new_code_quality = current.code_quality_score
    new_streak = current.streak_bonus
    exercises_completed = current.exercises_completed
    quizzes_taken = current.quizzes_taken

    if exercise_score is not None:
        new_exercises = calculate_ema(exercise_score, current.exercises_score)
        exercises_completed += 1

    if quiz_score is not None:
        new_quizzes = calculate_ema(quiz_score, current.quizzes_score, alpha=0.4)
        quizzes_taken += 1

    if code_quality is not None:
        new_code_quality = calculate_ema(code_quality, current.code_quality_score, alpha=0.2)

    if streak_days is not None:
        new_streak = calculate_streak_bonus(streak_days)

    return MasteryScore(
        student_id=current.student_id,
        topic_id=current.topic_id,
        topic_name=current.topic_name,
        exercises_score=round(new_exercises, 2),
        quizzes_score=round(new_quizzes, 2),
        code_quality_score=round(new_code_quality, 2),
        streak_bonus=round(new_streak, 2),
        exercises_completed=exercises_completed,
        quizzes_taken=quizzes_taken,
        last_activity=datetime.utcnow(),
    )


def create_initial_mastery(
    student_id: UUID,
    topic_id: str,
    topic_name: str,
) -> MasteryScore:
    """
    Create an initial mastery score for a new topic.

    Args:
        student_id: The student's ID
        topic_id: The topic identifier
        topic_name: Human-readable topic name

    Returns:
        New MasteryScore initialized to Beginner level
    """
    return MasteryScore(
        student_id=student_id,
        topic_id=topic_id,
        topic_name=topic_name,
        exercises_score=0,
        quizzes_score=0,
        code_quality_score=50,  # Neutral starting point
        streak_bonus=0,
        exercises_completed=0,
        quizzes_taken=0,
        last_activity=datetime.utcnow(),
    )


def calculate_overall_mastery(
    topic_scores: list[MasteryScore],
) -> float:
    """
    Calculate overall mastery across all topics.

    Args:
        topic_scores: List of mastery scores for all topics

    Returns:
        Weighted average mastery score (0-100)
    """
    if not topic_scores:
        return 0.0

    # Weight topics by activity (more exercises = more weight)
    total_weight = 0
    weighted_sum = 0

    for score in topic_scores:
        weight = max(1, score.exercises_completed + score.quizzes_taken)
        weighted_sum += score.total_score * weight
        total_weight += weight

    return round(weighted_sum / total_weight, 2) if total_weight > 0 else 0.0


def get_level_from_score(score: float) -> str:
    """
    Determine mastery level from numeric score.

    Args:
        score: Mastery score (0-100)

    Returns:
        Level string: Beginner, Learning, Proficient, or Mastered
    """
    if score >= 91:
        return "Mastered"
    elif score >= 71:
        return "Proficient"
    elif score >= 41:
        return "Learning"
    return "Beginner"


def detect_milestones(
    old_score: float,
    new_score: float,
    topic_name: str,
) -> list[dict[str, str]]:
    """
    Detect milestones when mastery crosses thresholds.

    Args:
        old_score: Previous mastery score
        new_score: New mastery score
        topic_name: Name of the topic

    Returns:
        List of milestone dicts with type and message
    """
    milestones = []
    thresholds = [
        (40, "halfway", f"Getting started with {topic_name}! Keep going!"),
        (50, "halfway", f"Halfway there on {topic_name}! Keep going!"),
        (70, "almost_mastered", f"Great progress on {topic_name}! You're in the Learning zone!"),
        (90, "almost_mastered", f"Amazing! You've nearly mastered {topic_name}!"),
        (100, "mastered", f"Congratulations! You've mastered {topic_name}!"),
    ]

    for threshold, milestone_type, message in thresholds:
        if old_score < threshold <= new_score:
            milestones.append({
                "milestone_type": milestone_type,
                "message": message,
                "threshold": threshold,
            })

    return milestones


def calculate_improvement_suggestions(
    mastery: MasteryScore,
) -> list[str]:
    """
    Generate improvement suggestions based on mastery breakdown.

    Args:
        mastery: Current mastery score

    Returns:
        List of actionable suggestions
    """
    suggestions = []

    if mastery.exercises_completed < 3:
        suggestions.append("Complete more exercises to build practical skills")

    if mastery.exercises_score < 60:
        suggestions.append("Focus on understanding exercise requirements before coding")

    if mastery.quizzes_taken < 2:
        suggestions.append("Take quizzes to reinforce theoretical knowledge")

    if mastery.quizzes_score < 60:
        suggestions.append("Review concept explanations before attempting quizzes")

    if mastery.code_quality_score < 60:
        suggestions.append("Pay attention to code style and PEP 8 guidelines")

    if mastery.streak_bonus < 30:
        suggestions.append("Practice daily to build momentum and retain knowledge")

    # If doing well, encourage advancement
    if mastery.total_score >= 70 and not suggestions:
        suggestions.append("Great progress! Try more challenging exercises")

    return suggestions[:3]  # Return top 3 suggestions
