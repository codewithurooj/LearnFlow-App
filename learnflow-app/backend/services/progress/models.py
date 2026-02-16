"""
Progress Service Models

Request and response models for the Progress API endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TopicMasteryResponse(BaseModel):
    """Summary of mastery for a single topic."""

    topic_id: str
    topic_name: str
    mastery_score: float = Field(ge=0, le=100)
    mastery_level: str = Field(pattern="^(Beginner|Learning|Proficient|Mastered)$")
    level_color: str


class MasteryBreakdownResponse(BaseModel):
    """Detailed breakdown of mastery components."""

    exercises_score: float = Field(ge=0, le=100)
    quizzes_score: float = Field(ge=0, le=100)
    code_quality_score: float = Field(ge=0, le=100)
    streak_bonus: float = Field(ge=0, le=100)
    exercises_completed: int = Field(ge=0)
    quizzes_taken: int = Field(ge=0)


class ProgressSummaryResponse(BaseModel):
    """Overall progress summary for a student."""

    student_id: UUID
    overall_mastery: float = Field(ge=0, le=100)
    overall_level: str
    topics: list[TopicMasteryResponse]
    current_streak: int = Field(ge=0)
    last_activity: datetime
    total_exercises: int = Field(ge=0)
    total_quizzes: int = Field(ge=0)


class TopicDetailResponse(BaseModel):
    """Detailed progress for a specific topic."""

    topic_id: str
    topic_name: str
    mastery_score: float = Field(ge=0, le=100)
    mastery_level: str
    level_color: str
    breakdown: MasteryBreakdownResponse
    improvement_suggestions: list[str] = Field(default_factory=list)
    last_activity: datetime


class StudentProgressState(BaseModel):
    """
    Complete progress state for a student stored in Dapr state.

    This is the internal storage model, not the API response.
    """

    student_id: UUID
    topics: dict[str, dict]  # topic_id -> MasteryScore dict
    current_streak: int = 0
    last_activity_date: Optional[str] = None  # ISO date string (YYYY-MM-DD)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class LowScoreAlertRequest(BaseModel):
    """Request model for reporting low quiz scores (struggle detection)."""

    student_id: UUID
    topic_id: str
    quiz_score: float = Field(ge=0, le=100)
    quiz_id: UUID
