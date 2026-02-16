"""
Kafka Event Schemas

Event models for pub/sub messaging between services.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from .struggle import StruggleType


class BaseEvent(BaseModel):
    """Base class for all Kafka events."""

    event_id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source_service: str
    correlation_id: Optional[UUID] = None

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v),
        }


class QuestionEvent(BaseEvent):
    """Event published when a student asks a question (learning.questions topic)."""

    source_service: str = "frontend"
    student_id: UUID
    session_id: UUID
    question_text: str


class ResponseEvent(BaseEvent):
    """Event published when an agent responds (learning.responses topic)."""

    student_id: UUID
    session_id: UUID
    question_id: UUID
    response_text: str
    agent_type: str  # triage, concepts, debug, code-review, exercise
    sources: list[str] = Field(default_factory=list)
    processing_time_ms: int


class CodeSubmissionEvent(BaseEvent):
    """Event published when student submits code (code.submissions topic)."""

    source_service: str = "frontend"
    student_id: UUID
    code: str
    exercise_id: Optional[UUID] = None


class CodeResultEvent(BaseEvent):
    """Event published after code execution (code.results topic)."""

    source_service: str = "code-runner"
    student_id: UUID
    submission_id: UUID
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: int
    memory_used_mb: float
    timed_out: bool
    error_type: Optional[str] = None


class StruggleDetectedEvent(BaseEvent):
    """Event published when struggle is detected (struggle.detected topic)."""

    source_service: str = "debug"
    student_id: UUID
    struggle_type: StruggleType
    topic_id: Optional[str] = None
    details: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)


class ProgressUpdatedEvent(BaseEvent):
    """Event published when mastery score changes (progress.updated topic)."""

    source_service: str = "progress"
    student_id: UUID
    topic_id: str
    old_score: float
    new_score: float
    old_level: str
    new_level: str
    level_changed: bool


class ExerciseCompletedEvent(BaseEvent):
    """Event published when an exercise is completed."""

    source_service: str = "exercise"
    student_id: UUID
    exercise_id: UUID
    topic_id: str
    passed: bool
    score: float
    time_spent_seconds: int


class QuizCompletedEvent(BaseEvent):
    """Event published when a quiz is completed."""

    source_service: str = "exercise"
    student_id: UUID
    quiz_id: UUID
    topic_id: str
    score: float
    questions_correct: int
    questions_total: int
