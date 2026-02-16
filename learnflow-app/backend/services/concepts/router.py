"""
Concepts Service Router

Endpoints for Python concept explanations.
"""

from typing import Any, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/concepts/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client, get_state, save_state
from shared.models import HealthResponse, Message

from agent import explain_concept
from adapters import get_mastery_adapter

router = APIRouter()
logger = structlog.get_logger(__name__)


class CodeExample(BaseModel):
    """A code example with explanation."""
    title: str
    code: str
    explanation: str


class ConceptsRequest(BaseModel):
    """Request for concept explanation."""
    student_id: UUID
    topic: str = Field(min_length=1, max_length=500)
    mastery_level: Optional[str] = Field(
        default="Beginner",
        pattern="^(Beginner|Learning|Proficient|Mastered)$",
    )
    context: list[Message] = Field(default_factory=list)


class ConceptsResponse(BaseModel):
    """Response with concept explanation."""
    explanation: str
    code_examples: list[CodeExample]
    related_topics: list[str]
    difficulty_adapted: bool


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="concepts",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.post("/concepts/explain", response_model=ConceptsResponse)
async def explain_python_concept(request: ConceptsRequest) -> ConceptsResponse:
    """
    Explain a Python concept adapted to student's mastery level.

    The explanation complexity is adjusted based on:
    - Beginner: Simple analogies, avoid jargon, more examples
    - Learning: Introduce technical terms, compare approaches
    - Proficient: Edge cases, performance considerations
    - Mastered: Advanced patterns, optimizations
    """
    logger.info(
        "Explaining concept",
        student_id=str(request.student_id),
        topic=request.topic,
        mastery_level=request.mastery_level,
    )

    # Get mastery adapter for response formatting
    adapter = get_mastery_adapter(request.mastery_level or "Beginner")

    # Get or create session context
    session_key = f"session:{request.student_id}"
    session_context = await get_state(session_key) or {"history": []}

    # Add current question to context
    context_messages = request.context or []
    context_messages.append(Message(role="user", content=request.topic))

    # Generate explanation
    result = await explain_concept(
        topic=request.topic,
        mastery_level=request.mastery_level or "Beginner",
        context=context_messages,
        adapter=adapter,
    )

    # Update session with response
    session_context["history"].append({
        "topic": request.topic,
        "mastery_level": request.mastery_level,
    })
    await save_state(session_key, session_context)

    return ConceptsResponse(
        explanation=result["explanation"],
        code_examples=[
            CodeExample(
                title=ex.get("title", "Example"),
                code=ex.get("code", ""),
                explanation=ex.get("explanation", ""),
            )
            for ex in result.get("examples", [])
        ],
        related_topics=result.get("related_topics", []),
        difficulty_adapted=True,
    )


@router.get("/concepts/topics")
async def get_available_topics() -> dict[str, list[str]]:
    """Get list of available Python topics by category."""
    return {
        "basics": [
            "variables", "data types", "operators", "strings",
            "lists", "tuples", "dictionaries", "sets",
        ],
        "control_flow": [
            "if statements", "for loops", "while loops",
            "break and continue", "match statements",
        ],
        "functions": [
            "function definition", "parameters and arguments",
            "return values", "lambda functions", "decorators",
            "generators", "recursion",
        ],
        "oop": [
            "classes and objects", "inheritance", "polymorphism",
            "encapsulation", "magic methods", "abstract classes",
        ],
        "advanced": [
            "context managers", "iterators", "metaclasses",
            "descriptors", "async/await", "type hints",
        ],
    }
