"""
Code Runner Service Router

Endpoints for sandboxed Python code execution.
"""

import time
from collections import defaultdict
from typing import Any, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/code-runner/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client, publish_event, get_state, save_state
from shared.models import HealthResponse
from shared.models.events import CodeResultEvent, CodeSubmissionEvent, StruggleDetectedEvent
from shared.models.struggle import StruggleType

from sandbox import execute_code, SandboxResult
from resource_limiter import ResourceLimiter

router = APIRouter()
logger = structlog.get_logger(__name__)

# Track consecutive failures per student
failure_tracker: dict[str, int] = defaultdict(int)


class CodeExecuteRequest(BaseModel):
    """Request for code execution."""
    student_id: UUID
    code: str = Field(min_length=1, max_length=50000)
    exercise_id: Optional[UUID] = None


class CodeExecuteResponse(BaseModel):
    """Response from code execution."""
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: int
    memory_used_mb: float
    timed_out: bool
    error_type: Optional[str] = None


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="code-runner",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.post("/code/execute", response_model=CodeExecuteResponse)
async def execute_python_code(request: CodeExecuteRequest) -> CodeExecuteResponse:
    """
    Execute Python code in a secure sandbox.

    Security constraints:
    - 5 second timeout
    - 50MB memory limit
    - No network access
    - Standard library imports only
    """
    logger.info(
        "Executing code",
        student_id=str(request.student_id),
        code_length=len(request.code),
    )

    start_time = time.time()

    # Execute in sandbox
    result = await execute_code(
        code=request.code,
        timeout=settings.code_execution_timeout,
        memory_limit_mb=settings.code_memory_limit_mb,
    )

    execution_time_ms = int((time.time() - start_time) * 1000)

    # Track failures for struggle detection
    student_key = str(request.student_id)
    if result.exit_code != 0 or result.timed_out:
        failure_tracker[student_key] += 1
        logger.info(
            "Execution failed",
            student_id=student_key,
            consecutive_failures=failure_tracker[student_key],
        )

        # Check for struggle threshold
        if failure_tracker[student_key] >= settings.struggle_failure_threshold:
            await _publish_struggle_alert(
                student_id=request.student_id,
                failure_count=failure_tracker[student_key],
                last_error=result.error_type,
            )
    else:
        # Reset on success
        failure_tracker[student_key] = 0

    # Publish result event
    await publish_event(
        topic=settings.topic_code_results,
        data=CodeResultEvent(
            source_service="code-runner",
            student_id=request.student_id,
            submission_id=request.student_id,  # Simplified
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.exit_code,
            execution_time_ms=execution_time_ms,
            memory_used_mb=result.memory_used_mb,
            timed_out=result.timed_out,
            error_type=result.error_type,
        ),
    )

    return CodeExecuteResponse(
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.exit_code,
        execution_time_ms=execution_time_ms,
        memory_used_mb=result.memory_used_mb,
        timed_out=result.timed_out,
        error_type=result.error_type,
    )


@router.post("/events/code-submissions")
async def handle_code_submission_event(event: dict[str, Any]) -> dict[str, str]:
    """Handle incoming code submission events from Dapr pub/sub."""
    try:
        data = event.get("data", {})
        submission = CodeSubmissionEvent.model_validate(data)

        # Execute the code
        result = await execute_python_code(
            CodeExecuteRequest(
                student_id=submission.student_id,
                code=submission.code,
                exercise_id=submission.exercise_id,
            )
        )

        logger.info(
            "Processed code submission",
            event_id=str(submission.event_id),
            success=result.exit_code == 0,
        )

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error("Failed to process code submission", error=str(e))
        return {"status": "DROP"}


async def _publish_struggle_alert(
    student_id: UUID,
    failure_count: int,
    last_error: Optional[str],
) -> None:
    """Publish a struggle alert for consecutive failures."""
    await publish_event(
        topic=settings.topic_struggle_detected,
        data=StruggleDetectedEvent(
            source_service="code-runner",
            student_id=student_id,
            struggle_type=StruggleType.FAILURES,
            details={
                "consecutive_failures": failure_count,
                "last_error_type": last_error,
                "threshold": settings.struggle_failure_threshold,
            },
            confidence=min(0.5 + (failure_count * 0.1), 0.95),
        ),
    )
    logger.warning(
        "Struggle alert published",
        student_id=str(student_id),
        failure_count=failure_count,
    )
