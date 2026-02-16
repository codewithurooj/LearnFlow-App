"""
Code Review Service Router

Endpoints for Python code review with 4-criteria evaluation.
"""

from typing import Any, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/code-review/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client, publish_event
from shared.models import HealthResponse

from agent import review_code

router = APIRouter()
logger = structlog.get_logger(__name__)


class CriterionScore(BaseModel):
    """Score and feedback for a single review criterion."""
    score: int = Field(ge=1, le=5)
    feedback: str


class ReviewRequest(BaseModel):
    """Request for code review."""
    student_id: UUID
    code: str = Field(min_length=1, max_length=10000)
    context: Optional[str] = None


class ReviewResponse(BaseModel):
    """Response with code review feedback."""
    rating: int = Field(ge=1, le=5)
    correctness: CriterionScore
    style: CriterionScore
    efficiency: CriterionScore
    readability: CriterionScore
    strengths: list[str]
    suggestions: list[str]
    encouragement: str


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="code-review",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.post("/review/analyze", response_model=ReviewResponse)
async def analyze_code(request: ReviewRequest) -> ReviewResponse:
    """
    Review Python code against 4 criteria with a 1-5 star rating.

    Criteria:
    1. Correctness - Does the code work as intended?
    2. Style (PEP 8) - Naming, spacing, imports
    3. Efficiency - Time/space complexity
    4. Readability - Clear names, comments, structure
    """
    logger.info(
        "Reviewing code",
        student_id=str(request.student_id),
        code_length=len(request.code),
    )

    try:
        result = await review_code(
            code=request.code,
            context=request.context or "",
        )
    except Exception as e:
        logger.error("Code review failed", error=str(e), student_id=str(request.student_id))
        raise HTTPException(status_code=503, detail="Code review service temporarily unavailable")

    def _parse_criterion(data: Any) -> CriterionScore:
        if isinstance(data, dict):
            return CriterionScore(
                score=max(1, min(5, int(data.get("score", 3)))),
                feedback=str(data.get("feedback", "No feedback available.")),
            )
        return CriterionScore(score=3, feedback="No feedback available.")

    # Publish code.reviewed event for progress tracking
    try:
        await publish_event(
            topic="code.reviewed",
            data={
                "student_id": str(request.student_id),
                "rating": result["rating"],
                "code_quality_score": result["rating"] * 20,  # Convert 1-5 to 0-100
            },
        )
    except Exception as e:
        logger.warning("Failed to publish code.reviewed event", error=str(e))

    return ReviewResponse(
        rating=result["rating"],
        correctness=_parse_criterion(result["correctness"]),
        style=_parse_criterion(result["style"]),
        efficiency=_parse_criterion(result["efficiency"]),
        readability=_parse_criterion(result["readability"]),
        strengths=result.get("strengths", []),
        suggestions=result.get("suggestions", []),
        encouragement=result.get("encouragement", "Keep coding!"),
    )


@router.post("/events/code-submitted")
async def handle_code_submitted(event: dict[str, Any]) -> dict[str, str]:
    """Handle incoming code submission events from Dapr pub/sub."""
    try:
        data = event.get("data", {})
        student_id = data.get("student_id", "unknown")
        code = data.get("code", "")

        if not code:
            logger.warning("Empty code in submission event", student_id=student_id)
            return {"status": "DROP"}

        result = await review_code(code=code, context=data.get("context", ""))

        await publish_event(
            topic="code.reviewed",
            data={
                "student_id": student_id,
                "rating": result["rating"],
                "code_quality_score": result["rating"] * 20,
            },
        )

        logger.info("Processed code submission event", student_id=student_id, rating=result["rating"])
        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error("Failed to process code submission event", error=str(e))
        return {"status": "RETRY"}
