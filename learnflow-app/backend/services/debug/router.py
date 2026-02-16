"""
Debug Service Router

Endpoints for debugging assistance and error analysis.
"""

from typing import Any, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/debug/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client, publish_event
from shared.models import HealthResponse
from shared.models.events import StruggleDetectedEvent
from shared.models.struggle import StruggleType

from error_parser import parse_traceback, ErrorInfo
from struggle_detector import StruggleDetector
from agent import analyze_error

router = APIRouter()
logger = structlog.get_logger(__name__)

# Global struggle detector
struggle_detector = StruggleDetector()


class DebugRequest(BaseModel):
    """Request for error debugging."""
    student_id: UUID
    code: str
    error_output: str
    traceback: Optional[str] = None


class DebugResponse(BaseModel):
    """Response with debugging assistance."""
    error_type: str
    error_line: Optional[int] = None
    root_cause: str
    hint: str
    solution: Optional[str] = None
    struggle_detected: bool


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="debug",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.post("/debug/analyze", response_model=DebugResponse)
async def analyze_debug_request(request: DebugRequest) -> DebugResponse:
    """
    Analyze an error and provide debugging assistance.

    Approach: Hints before solutions
    1. Identify the error type and line
    2. Explain why this error occurs
    3. Provide a hint that guides without revealing the answer
    4. Only reveal solution if specifically requested
    """
    logger.info(
        "Analyzing error",
        student_id=str(request.student_id),
        error_preview=request.error_output[:100],
    )

    # Parse the traceback
    traceback_text = request.traceback or request.error_output
    error_info = parse_traceback(traceback_text)

    # Check for struggle pattern
    struggle_detected = struggle_detector.record_error(
        student_id=request.student_id,
        error_type=error_info.error_type,
    )

    if struggle_detected:
        await _publish_struggle_alert(
            student_id=request.student_id,
            error_type=error_info.error_type,
            error_count=struggle_detector.get_error_count(
                request.student_id,
                error_info.error_type,
            ),
        )

    # Get AI analysis
    analysis = await analyze_error(
        code=request.code,
        error_info=error_info,
        error_output=request.error_output,
    )

    return DebugResponse(
        error_type=error_info.error_type,
        error_line=error_info.line_number,
        root_cause=analysis.get("root_cause", f"A {error_info.error_type} occurred"),
        hint=analysis.get("hint", "Check the error message carefully"),
        solution=None,  # Don't reveal solution initially
        struggle_detected=struggle_detected,
    )


@router.post("/debug/solution")
async def get_solution(request: DebugRequest) -> dict[str, str]:
    """
    Get the full solution for an error.

    Only called when student explicitly requests the solution
    after trying with hints.
    """
    logger.info(
        "Providing solution",
        student_id=str(request.student_id),
    )

    traceback_text = request.traceback or request.error_output
    error_info = parse_traceback(traceback_text)

    analysis = await analyze_error(
        code=request.code,
        error_info=error_info,
        error_output=request.error_output,
        include_solution=True,
    )

    return {
        "solution": analysis.get("solution", "Review your code carefully"),
        "corrected_code": analysis.get("corrected_code", ""),
    }


async def _publish_struggle_alert(
    student_id: UUID,
    error_type: str,
    error_count: int,
) -> None:
    """Publish a struggle alert for repeated errors."""
    await publish_event(
        topic=settings.topic_struggle_detected,
        data=StruggleDetectedEvent(
            source_service="debug",
            student_id=student_id,
            struggle_type=StruggleType.ERROR_PATTERN,
            details={
                "error_type": error_type,
                "error_count": error_count,
                "threshold": settings.struggle_error_threshold,
            },
            confidence=min(0.6 + (error_count * 0.1), 0.95),
        ),
    )
    logger.warning(
        "Struggle alert published for error pattern",
        student_id=str(student_id),
        error_type=error_type,
        count=error_count,
    )
