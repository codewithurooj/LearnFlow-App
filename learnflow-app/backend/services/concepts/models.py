"""
Concepts Service Models

Request and response models for the Concepts API.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/concepts/models.py", ""))

from shared.models import Message


class CodeExample(BaseModel):
    """A code example with explanation."""

    title: str = Field(description="Brief title for the example")
    code: str = Field(description="Python code")
    explanation: str = Field(description="What the code does and why")


class ConceptsRequest(BaseModel):
    """Request for concept explanation."""

    student_id: UUID
    topic: str = Field(min_length=1, max_length=500, description="The Python concept to explain")
    mastery_level: Optional[str] = Field(
        default="Beginner",
        pattern="^(Beginner|Learning|Proficient|Mastered)$",
        description="Student's current mastery level",
    )
    context: list[Message] = Field(
        default_factory=list,
        description="Previous conversation messages for context",
    )


class ConceptsResponse(BaseModel):
    """Response with concept explanation."""

    explanation: str = Field(description="Markdown-formatted explanation")
    code_examples: list[CodeExample] = Field(
        description="Runnable code examples demonstrating the concept"
    )
    related_topics: list[str] = Field(
        description="Suggested topics to explore next"
    )
    difficulty_adapted: bool = Field(
        description="Whether the response was adapted to mastery level"
    )
