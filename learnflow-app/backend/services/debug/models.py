"""
Debug Service Models

Request and response models for the Debug API.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class DebugRequest(BaseModel):
    """Request for error debugging."""

    student_id: UUID
    code: str = Field(description="The student's code with the error")
    error_output: str = Field(description="The error message or traceback")
    traceback: Optional[str] = Field(
        default=None,
        description="Full traceback if available separately",
    )


class DebugResponse(BaseModel):
    """Response with debugging assistance."""

    error_type: str = Field(description="The Python error type")
    error_line: Optional[int] = Field(
        default=None,
        description="Line number where error occurred",
    )
    root_cause: str = Field(description="Explanation of why the error occurred")
    hint: str = Field(description="Hint to help fix without revealing solution")
    solution: Optional[str] = Field(
        default=None,
        description="Solution (only provided on explicit request)",
    )
    struggle_detected: bool = Field(
        description="Whether a struggle pattern was detected",
    )


class SolutionResponse(BaseModel):
    """Response with full solution."""

    solution: str = Field(description="Explanation of how to fix the error")
    corrected_code: str = Field(description="The corrected code")
