"""
Triage Service Router

Endpoints for question routing, classification, and Dapr event handling.
"""

import time
from typing import Any, Optional
from uuid import UUID

import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/triage/router.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client, publish_event
from shared.models import HealthResponse, Message
from shared.models.events import QuestionEvent, ResponseEvent
from shared.models.question import RoutingDecision
from shared.agents.registry import get_registry

from classifier import classify_question, ClassificationResult
from agent import classify_hybrid

router = APIRouter()
logger = structlog.get_logger(__name__)
registry = get_registry()


class TriageRequest(BaseModel):
    """Request for question routing."""
    student_id: UUID
    question: str = Field(min_length=1, max_length=5000)
    session_id: Optional[UUID] = None
    mastery_level: Optional[str] = "Beginner"


class ClassifyResponse(BaseModel):
    """Response from classification only."""
    routed_to: str
    confidence: float = Field(ge=0, le=1)
    method: str
    keywords_matched: list[str] = Field(default_factory=list)
    clarifying_question: Optional[str] = None


class TriageResponse(BaseModel):
    """Response from triage routing."""
    routed_to: str
    confidence: float = Field(ge=0, le=1)
    response: str
    sources: list[str] = Field(default_factory=list)
    processing_time_ms: int


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint for Kubernetes probes."""
    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()

    return HealthResponse(
        status="healthy" if dapr_healthy else "degraded",
        service="triage",
        version=settings.service_version,
        dapr_connected=dapr_healthy,
    )


@router.post("/triage/classify", response_model=ClassifyResponse)
async def classify_only(request: TriageRequest) -> ClassifyResponse:
    """
    Classify a question without routing to specialist.

    Returns the routing decision with confidence and method used.
    """
    keyword_result = classify_question(request.question)
    classification = await classify_hybrid(request.question, keyword_result)

    clarifying = None
    if classification.confidence < 0.7:
        clarifying = "Could you clarify what you'd like help with? Are you looking for a concept explanation, debugging help, a code review, practice exercises, or a progress update?"

    return ClassifyResponse(
        routed_to=classification.category,
        confidence=classification.confidence,
        method=classification.method,
        keywords_matched=classification.keywords_matched,
        clarifying_question=clarifying,
    )


@router.post("/triage/route", response_model=TriageResponse)
async def route_question(request: TriageRequest) -> TriageResponse:
    """
    Route a student question to the appropriate specialist agent.

    1. First attempts keyword-based classification
    2. Falls back to AI classification if uncertain
    3. Invokes the specialist service via Dapr
    4. Returns aggregated response
    """
    start_time = time.time()

    logger.info(
        "Routing question",
        student_id=str(request.student_id),
        question_preview=request.question[:100],
    )

    # Step 1: Hybrid classification (keyword + AI fallback)
    keyword_result = classify_question(request.question)
    classification = await classify_hybrid(request.question, keyword_result)

    logger.info(
        "Classification result",
        routed_to=classification.category,
        confidence=classification.confidence,
        method=classification.method,
    )

    # Step 2: Invoke specialist service via Dapr
    dapr = get_dapr_client()
    specialist_response = ""
    sources: list[str] = []

    try:
        app_id = registry.get_service_app_id(classification.category)
        endpoint = registry.get_service_endpoint(classification.category)

        if classification.category == "concepts":
            result = await dapr.invoke_service(
                app_id=app_id,
                method=endpoint,
                data={
                    "student_id": str(request.student_id),
                    "topic": request.question,
                    "mastery_level": request.mastery_level,
                },
            )
            specialist_response = result.get("explanation", "")
            sources = result.get("related_concepts", [])

        elif classification.category == "debug":
            result = await dapr.invoke_service(
                app_id=app_id,
                method=endpoint,
                data={
                    "student_id": str(request.student_id),
                    "code": "",
                    "error_output": request.question,
                },
            )
            specialist_response = f"{result.get('root_cause', '')}\n\nHint: {result.get('hint', '')}"

        elif classification.category == "code_review":
            result = await dapr.invoke_service(
                app_id=app_id,
                method=endpoint,
                data={
                    "student_id": str(request.student_id),
                    "code": request.question,
                },
            )
            specialist_response = f"Rating: {result.get('rating', '?')}/5\n\n{result.get('feedback', '')}"

        elif classification.category == "exercise":
            result = await dapr.invoke_service(
                app_id=app_id,
                method=endpoint,
                data={
                    "student_id": str(request.student_id),
                    "topic": request.question,
                    "mastery_level": request.mastery_level,
                },
            )
            specialist_response = f"Here's an exercise for you:\n\n{result.get('prompt', result.get('description', ''))}"

        elif classification.category == "progress":
            result = await dapr.invoke_service(
                app_id=app_id,
                method=f"api/v1/progress/{request.student_id}",
                http_verb="GET",
            )
            specialist_response = f"Overall mastery: {result.get('overall_mastery', 0)}%\n\n{result.get('summary', '')}"

        else:
            specialist_response = f"I understand you're asking about: {request.question}. Let me help you with that concept."

    except Exception as e:
        logger.error("Failed to invoke specialist", error=str(e), agent=classification.category)
        specialist_response = (
            f"I'm having trouble connecting to the {classification.category} specialist. "
            f"Your question relates to {classification.category}. Please try again shortly."
        )

    processing_time = int((time.time() - start_time) * 1000)

    # Step 3: Publish response event
    await publish_event(
        topic=settings.topic_learning_responses,
        data=ResponseEvent(
            source_service="triage",
            student_id=request.student_id,
            session_id=request.session_id or request.student_id,
            question_id=request.student_id,
            response_text=specialist_response,
            agent_type=classification.category,
            sources=sources,
            processing_time_ms=processing_time,
        ),
    )

    return TriageResponse(
        routed_to=classification.category,
        confidence=classification.confidence,
        response=specialist_response,
        sources=sources,
        processing_time_ms=processing_time,
    )


@router.post("/events/learning-questions")
async def handle_question_event(event: dict[str, Any]) -> dict[str, str]:
    """Handle incoming question events from Dapr pub/sub."""
    try:
        data = event.get("data", {})
        question_event = QuestionEvent.model_validate(data)

        result = await route_question(
            TriageRequest(
                student_id=question_event.student_id,
                question=question_event.question_text,
                session_id=question_event.session_id,
            )
        )

        logger.info(
            "Processed question event",
            event_id=str(question_event.event_id),
            routed_to=result.routed_to,
        )

        return {"status": "SUCCESS"}

    except Exception as e:
        logger.error("Failed to process question event", error=str(e))
        return {"status": "DROP"}
