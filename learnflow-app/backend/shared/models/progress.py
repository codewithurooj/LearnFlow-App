"""
Progress and Mastery Models

Models for tracking student progress and mastery scores.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, computed_field


class MasteryScore(BaseModel):
    """Student's mastery level for a specific topic."""

    student_id: UUID
    topic_id: str
    topic_name: str

    # Component scores (0-100 scale)
    exercises_score: float = Field(default=0, ge=0, le=100)
    quizzes_score: float = Field(default=0, ge=0, le=100)
    code_quality_score: float = Field(default=0, ge=0, le=100)
    streak_bonus: float = Field(default=0, ge=0, le=100)

    # Tracking
    exercises_completed: int = Field(default=0, ge=0)
    quizzes_taken: int = Field(default=0, ge=0)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

    @computed_field
    @property
    def total_score(self) -> float:
        """Calculate weighted mastery score (0-100)."""
        return round(
            0.4 * self.exercises_score
            + 0.3 * self.quizzes_score
            + 0.2 * self.code_quality_score
            + 0.1 * self.streak_bonus,
            2,
        )

    @computed_field
    @property
    def level(self) -> str:
        """Determine mastery level from score."""
        score = self.total_score
        if score >= 91:
            return "Mastered"
        elif score >= 71:
            return "Proficient"
        elif score >= 41:
            return "Learning"
        return "Beginner"

    @computed_field
    @property
    def level_color(self) -> str:
        """Color code for the mastery level."""
        return {
            "Beginner": "red",
            "Learning": "yellow",
            "Proficient": "green",
            "Mastered": "blue",
        }[self.level]


class TopicProgress(BaseModel):
    """Summary of progress for a single topic."""

    topic_id: str
    topic_name: str
    mastery_score: float
    mastery_level: str
    level_color: str


class ProgressSummary(BaseModel):
    """Overall progress summary for a student."""

    student_id: UUID
    overall_mastery: float
    current_level: str
    topics: list[TopicProgress]
    current_streak: int
    last_activity: datetime


class MilestoneEvent(BaseModel):
    """A milestone achievement by a student."""

    student_id: UUID
    topic_id: str
    milestone_type: str  # "first_exercise" | "halfway" | "almost_mastered" | "mastered" | "streak"
    message: str
    old_score: float = 0.0
    new_score: float = 0.0
    achieved_at: datetime = Field(default_factory=datetime.utcnow)


class TopicDetail(BaseModel):
    """Detailed progress for a specific topic."""

    topic_id: str
    topic_name: str
    mastery_score: float
    mastery_level: str
    breakdown: MasteryScore
    improvement_suggestions: list[str] = Field(default_factory=list)
