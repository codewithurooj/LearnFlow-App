"""
Code Submission Models

Models for student code submissions and execution results.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Status of code execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    MEMORY_EXCEEDED = "memory_exceeded"
    SECURITY_VIOLATION = "security_violation"


class CodeSubmission(BaseModel):
    """Student code submitted for execution."""

    submission_id: UUID = Field(default_factory=uuid4)
    student_id: UUID
    code: str = Field(min_length=1, max_length=50000)
    language: str = Field(default="python", pattern="^python$")  # MVP: Python only
    exercise_id: Optional[UUID] = None

    # Execution results (populated after execution)
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    exit_code: Optional[int] = None
    execution_time_ms: Optional[int] = None
    memory_used_mb: Optional[float] = None
    status: ExecutionStatus = ExecutionStatus.PENDING
    error_type: Optional[str] = None  # SyntaxError, NameError, etc.

    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    executed_at: Optional[datetime] = None

    @property
    def is_success(self) -> bool:
        """Check if execution was successful."""
        return self.status == ExecutionStatus.SUCCESS and self.exit_code == 0

    @property
    def has_error(self) -> bool:
        """Check if execution produced an error."""
        return self.status in (
            ExecutionStatus.ERROR,
            ExecutionStatus.TIMEOUT,
            ExecutionStatus.MEMORY_EXCEEDED,
            ExecutionStatus.SECURITY_VIOLATION,
        )
