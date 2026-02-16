"""
Struggle Detection Models

Models for tracking student struggles and generating alerts.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class StruggleType(str, Enum):
    """Types of struggle patterns that can be detected."""

    ERROR_PATTERN = "error_pattern"  # 3+ same error type
    STUCK = "stuck"  # >10 minutes on exercise
    LOW_SCORE = "low_score"  # Quiz score <50%
    FRUSTRATION = "frustration"  # Keywords detected
    FAILURES = "failures"  # 5+ consecutive execution failures


class StruggleAlert(BaseModel):
    """Alert when a student is struggling."""

    alert_id: UUID = Field(default_factory=uuid4)
    student_id: UUID
    struggle_type: StruggleType
    topic_id: Optional[str] = None
    details: dict[str, Any] = Field(default_factory=dict)
    confidence: float = Field(ge=0, le=1)
    resolved: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None

    def resolve(self) -> None:
        """Mark the alert as resolved."""
        self.resolved = True
        self.resolved_at = datetime.utcnow()


class ErrorRecord(BaseModel):
    """A single error occurrence for struggle tracking."""

    error_type: str
    error_message: str = ""
    line_number: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class StudentStruggleState(BaseModel):
    """Per-student struggle tracking state stored in Dapr state store."""

    student_id: UUID
    error_history: list[ErrorRecord] = Field(default_factory=list)
    consecutive_failures: int = 0
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    stuck_since: Optional[datetime] = None
    frustration_keywords_detected: bool = False

    def add_error(self, error: ErrorRecord, window_minutes: int = 30) -> None:
        """Add an error and prune entries outside the sliding window."""
        self.error_history.append(error)
        self.last_activity = datetime.utcnow()
        cutoff = datetime.utcnow() - __import__("datetime").timedelta(minutes=window_minutes)
        self.error_history = [e for e in self.error_history if e.timestamp >= cutoff]

    def count_error_type(self, error_type: str) -> int:
        """Count occurrences of a specific error type in the window."""
        return sum(1 for e in self.error_history if e.error_type == error_type)


class StrugglePattern(BaseModel):
    """Pattern data used for struggle detection."""

    student_id: UUID
    error_type: Optional[str] = None
    error_count: int = 0
    failure_count: int = 0
    exercise_start_time: Optional[datetime] = None
    last_error_time: Optional[datetime] = None
    window_minutes: int = 30
