"""
Context Provider for MCP Server

Aggregates data from Dapr state stores and Kafka topics
to provide rich context for AI agent debugging and expansion.
"""

import json
from typing import Any, Optional

import httpx
import structlog

import sys

sys.path.insert(0, str(__file__).replace("services/mcp-context/context_provider.py", ""))

from shared.config import settings

logger = structlog.get_logger(__name__)


class ContextProvider:
    """Provides contextual data from LearnFlow services."""

    def __init__(self):
        self._http_client: Optional[httpx.AsyncClient] = None
        self._dapr_url = settings.dapr_http_url

    async def initialize(self):
        """Initialize HTTP client for Dapr sidecar communication."""
        self._http_client = httpx.AsyncClient(timeout=10.0)
        logger.info("Context provider initialized", dapr_url=self._dapr_url)

    async def close(self):
        """Clean up HTTP client."""
        if self._http_client:
            await self._http_client.aclose()

    async def get_student_progress(self, student_id: str) -> dict[str, Any]:
        """Fetch student progress from Dapr state store."""
        try:
            url = f"{self._dapr_url}/v1.0/state/{settings.dapr_statestore_name}/progress-{student_id}"
            resp = await self._http_client.get(url)
            if resp.status_code == 200 and resp.text:
                return json.loads(resp.text)
            return {"student_id": student_id, "status": "no_data"}
        except Exception as e:
            logger.error("Failed to fetch student progress", error=str(e))
            return {"student_id": student_id, "error": str(e)}

    async def get_student_struggles(self, student_id: str) -> dict[str, Any]:
        """Fetch struggle history for a student."""
        try:
            url = f"{self._dapr_url}/v1.0/state/{settings.dapr_statestore_name}/struggles-{student_id}"
            resp = await self._http_client.get(url)
            if resp.status_code == 200 and resp.text:
                return json.loads(resp.text)
            return {"student_id": student_id, "struggles": []}
        except Exception as e:
            logger.error("Failed to fetch struggles", error=str(e))
            return {"student_id": student_id, "error": str(e)}

    async def get_recent_submissions(
        self, student_id: str, limit: int = 10
    ) -> dict[str, Any]:
        """Fetch recent code submissions for a student."""
        try:
            url = f"{self._dapr_url}/v1.0/state/{settings.dapr_statestore_name}/submissions-{student_id}"
            resp = await self._http_client.get(url)
            if resp.status_code == 200 and resp.text:
                data = json.loads(resp.text)
                if isinstance(data, list):
                    return {"student_id": student_id, "submissions": data[:limit]}
                return data
            return {"student_id": student_id, "submissions": []}
        except Exception as e:
            logger.error("Failed to fetch submissions", error=str(e))
            return {"student_id": student_id, "error": str(e)}

    async def get_class_overview(self) -> dict[str, Any]:
        """Fetch aggregated class progress data."""
        try:
            url = f"{self._dapr_url}/v1.0/state/{settings.dapr_statestore_name}/class-overview"
            resp = await self._http_client.get(url)
            if resp.status_code == 200 and resp.text:
                return json.loads(resp.text)
            return {"total_students": 0, "active_struggles": 0}
        except Exception as e:
            logger.error("Failed to fetch class overview", error=str(e))
            return {"error": str(e)}

    async def get_service_health(self) -> dict[str, Any]:
        """Check health of all LearnFlow services."""
        services = {
            "triage": 8001,
            "concepts": 8002,
            "code-review": 8003,
            "debug": 8004,
            "exercise": 8005,
            "progress": 8006,
            "code-runner": 8007,
        }
        health = {}
        for name, port in services.items():
            try:
                resp = await self._http_client.get(
                    f"http://localhost:{port}/health", timeout=2.0
                )
                health[name] = "healthy" if resp.status_code == 200 else "unhealthy"
            except Exception:
                health[name] = "unreachable"
        return health

    async def get_system_context(self) -> dict[str, Any]:
        """Get full system context for AI agent debugging."""
        service_health = await self.get_service_health()
        class_overview = await self.get_class_overview()

        return {
            "system": {
                "services": service_health,
                "kafka_topics": [
                    settings.topic_learning_questions,
                    settings.topic_learning_responses,
                    settings.topic_code_submissions,
                    settings.topic_code_results,
                    settings.topic_struggle_detected,
                    settings.topic_progress_updated,
                ],
                "environment": settings.environment,
            },
            "class": class_overview,
        }
