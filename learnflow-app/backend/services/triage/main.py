"""
LearnFlow Triage Service

Entry point for the question routing microservice.
Routes student questions to appropriate specialist agents.
"""

import logging
import sys
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# Add shared library to path
sys.path.insert(0, str(__file__).replace("services/triage/main.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client

from router import router
from auth_router import auth_router, close_pool as close_auth_pool

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("Starting Triage Service", version=settings.service_version)

    # Check Dapr connection (non-fatal — service works without Dapr)
    try:
        dapr = get_dapr_client()
        dapr_healthy = await dapr.health_check()
        logger.info("Dapr sidecar status", connected=dapr_healthy)
    except Exception:
        logger.warning("Dapr sidecar not available, running without Dapr")

    yield

    # Cleanup
    try:
        dapr = get_dapr_client()
        await dapr.close()
    except Exception:
        pass
    await close_auth_pool()
    logger.info("Triage Service shutting down")


app = FastAPI(
    title="LearnFlow Triage Service",
    description="Routes student questions to specialist AI tutoring agents",
    version=settings.service_version,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logger.error("Validation error", body=body.decode(), errors=str(exc.errors()), url=str(request.url))
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Include routers
app.include_router(router, prefix="/api/v1")
app.include_router(auth_router)


@app.get("/dapr/subscribe")
async def get_subscriptions():
    """Return Dapr pub/sub subscriptions."""
    return [
        {
            "pubsubname": settings.dapr_pubsub_name,
            "topic": settings.topic_learning_questions,
            "route": "/events/learning-questions",
        }
    ]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=8001,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
