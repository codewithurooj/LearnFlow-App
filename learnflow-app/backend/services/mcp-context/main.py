"""
LearnFlow MCP Context Server

Provides AI agents with real-time access to student progress,
code submissions, struggle data, and system health via MCP protocol.
Enables AI-powered debugging and system expansion.
"""

import logging
import sys
from contextlib import asynccontextmanager

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

sys.path.insert(0, str(__file__).replace("services/mcp-context/main.py", ""))

from shared.config import settings

from router import router
from context_provider import ContextProvider

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
    logger.info("Starting MCP Context Server", version=settings.service_version)

    # Initialize context provider
    app.state.context_provider = ContextProvider()
    await app.state.context_provider.initialize()

    yield

    await app.state.context_provider.close()
    logger.info("MCP Context Server shutting down")


app = FastAPI(
    title="LearnFlow MCP Context Server",
    description="Provides real-time context to AI agents for debugging and expansion",
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

app.include_router(router, prefix="/api/v1/context")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "mcp-context"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=8008,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )
