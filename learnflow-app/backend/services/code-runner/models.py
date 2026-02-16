"""
Code Runner Service Models

Request and response models for the Code Runner API.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CodeExecuteRequest(BaseModel):
    """Request for code execution."""

    student_id: UUID
    code: str = Field(
        min_length=1,
        max_length=50000,
        description="Python code to execute",
    )
    exercise_id: Optional[UUID] = Field(
        default=None,
        description="Associated exercise ID if this is an exercise submission",
    )


class CodeExecuteResponse(BaseModel):
    """Response from code execution."""

    stdout: str = Field(description="Standard output from code execution")
    stderr: str = Field(description="Standard error output")
    exit_code: int = Field(description="Process exit code (0 = success)")
    execution_time_ms: int = Field(description="Execution time in milliseconds")
    memory_used_mb: float = Field(description="Memory used in megabytes")
    timed_out: bool = Field(description="Whether execution was terminated due to timeout")
    error_type: Optional[str] = Field(
        default=None,
        description="Type of Python error if one occurred",
    )


class SandboxConfig(BaseModel):
    """Configuration for the sandbox environment."""

    timeout_seconds: int = Field(default=5, ge=1, le=30)
    memory_limit_mb: int = Field(default=50, ge=10, le=100)
    allowed_imports: list[str] = Field(default_factory=list)
    blocked_builtins: list[str] = Field(default_factory=list)
