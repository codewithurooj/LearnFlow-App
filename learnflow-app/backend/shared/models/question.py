"""
Question Model

Model for student questions submitted for routing and answering.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class RoutingDecision(BaseModel):
    """Result of triage routing classification."""

    question_id: UUID = Field(default_factory=uuid4)
    routed_to: str  # concepts | debug | code_review | exercise | progress
    confidence: float = Field(ge=0.0, le=1.0)
    method: str = "keyword"  # "keyword" | "ai_fallback"
    keywords_matched: list[str] = Field(default_factory=list)
    clarifying_question: Optional[str] = None


class Question(BaseModel):
    """A student's question submitted for routing and answering."""

    question_id: UUID = Field(default_factory=uuid4)
    student_id: UUID
    session_id: UUID
    question_text: str = Field(min_length=1, max_length=5000)
    routed_to: Optional[str] = None  # concepts, debug, code-review, exercise
    routing_confidence: Optional[float] = Field(default=None, ge=0, le=1)
    response_text: Optional[str] = None
    response_sources: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    responded_at: Optional[datetime] = None

    @property
    def is_answered(self) -> bool:
        """Check if the question has been answered."""
        return self.response_text is not None

    @property
    def response_time_ms(self) -> Optional[int]:
        """Calculate response time in milliseconds."""
        if self.responded_at and self.created_at:
            delta = self.responded_at - self.created_at
            return int(delta.total_seconds() * 1000)
        return None
