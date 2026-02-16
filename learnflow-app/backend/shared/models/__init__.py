"""
LearnFlow Shared Models

Pydantic models shared across all LearnFlow backend microservices.
"""

from datetime import datetime
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


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


class Message(BaseModel):
    """A single message in a conversation."""

    role: str = Field(pattern="^(user|assistant|system)$")
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    agent_type: Optional[str] = None


class HealthResponse(BaseModel):
    """Standard health check response."""

    status: str = Field(pattern="^(healthy|degraded|unhealthy)$")
    service: str
    version: str
    dapr_connected: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


# Re-export all models for convenience
from .code_submission import CodeSubmission, ExecutionStatus
from .events import (
    CodeResultEvent,
    CodeSubmissionEvent,
    ExerciseCompletedEvent,
    ProgressUpdatedEvent,
    QuestionEvent,
    QuizCompletedEvent,
    ResponseEvent,
    StruggleDetectedEvent,
)
from .exercise import Difficulty, Exercise, ExerciseAttempt, GradeResult, TestCase, TestResult
from .progress import MasteryScore, MilestoneEvent, ProgressSummary
from .question import Question, RoutingDecision
from .struggle import ErrorRecord, StudentStruggleState, StruggleAlert, StruggleType
from .student import Student, StudentSession

__all__ = [
    # Base
    "BaseEvent",
    "Message",
    "HealthResponse",
    # Student
    "Student",
    "StudentSession",
    # Question
    "Question",
    "RoutingDecision",
    # Code
    "CodeSubmission",
    "ExecutionStatus",
    # Exercise
    "Exercise",
    "ExerciseAttempt",
    "TestCase",
    "TestResult",
    "Difficulty",
    # Exercise (additional)
    "GradeResult",
    # Progress
    "MasteryScore",
    "MilestoneEvent",
    "ProgressSummary",
    # Struggle
    "ErrorRecord",
    "StudentStruggleState",
    "StruggleAlert",
    "StruggleType",
    # Events
    "QuestionEvent",
    "ResponseEvent",
    "CodeSubmissionEvent",
    "CodeResultEvent",
    "StruggleDetectedEvent",
    "ProgressUpdatedEvent",
    "ExerciseCompletedEvent",
    "QuizCompletedEvent",
]
