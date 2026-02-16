"""
Triage Service Models

Request and response models for the Triage API.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TriageRequest(BaseModel):
    """Request for question routing."""

    student_id: UUID
    question: str = Field(min_length=1, max_length=5000)
    session_id: Optional[UUID] = None
    mastery_level: Optional[str] = Field(
        default="Beginner",
        pattern="^(Beginner|Learning|Proficient|Mastered)$",
    )


class TriageResponse(BaseModel):
    """Response from triage routing."""

    routed_to: str = Field(description="The specialist agent that handled the question")
    confidence: float = Field(ge=0, le=1, description="Confidence in routing decision")
    response: str = Field(description="The specialist's response")
    sources: list[str] = Field(default_factory=list, description="Related topics or sources")
    processing_time_ms: int = Field(description="Total processing time in milliseconds")


class RoutingDecision(BaseModel):
    """Internal routing decision details."""

    question_id: UUID
    routed_to: str
    confidence: float
    keywords_matched: list[str]
    fallback_used: bool
    reasoning: str
