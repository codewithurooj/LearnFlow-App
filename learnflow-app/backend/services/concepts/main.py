"""
LearnFlow Concepts Service

AI-powered Python concept explanation service.
Adapts explanations based on student mastery level.
"""

import logging
import sys
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(__file__).replace("services/concepts/main.py", ""))

from shared.config import settings
from shared.dapr import get_dapr_client

from router import router

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
    logger.info("Starting Concepts Service", version=settings.service_version)

    dapr = get_dapr_client()
    dapr_healthy = await dapr.health_check()
    logger.info("Dapr sidecar status", connected=dapr_healthy)

    yield

    await dapr.close()
    logger.info("Concepts Service shutting down")


app = FastAPI(
    title="LearnFlow Concepts Service",
    description="AI-powered Python concept explanations adapted to student level",
    version=settings.service_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=8002,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
