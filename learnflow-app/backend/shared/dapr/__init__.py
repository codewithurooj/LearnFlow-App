"""
Dapr Client Utilities

Centralized Dapr client initialization and common operations.
"""

import logging
from typing import Any, Optional

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


class DaprClient:
    """HTTP client for Dapr sidecar communication with direct fallback."""

    # Direct service URLs for Docker Compose (no Dapr sidecar)
    DIRECT_SERVICE_MAP = {
        "concepts-service": "http://concepts:8002",
        "debug-service": "http://debug:8004",
        "code-review-service": "http://code-review:8007",
        "exercise-service": "http://exercise:8005",
        "progress-service": "http://progress:8006",
        "triage-service": "http://triage:8001",
    }

    def __init__(self, dapr_http_port: Optional[int] = None):
        self.base_url = f"http://localhost:{dapr_http_port or settings.dapr_http_port}"
        self._client: Optional[httpx.AsyncClient] = None
        self._direct_client: Optional[httpx.AsyncClient] = None
        self._dapr_available: Optional[bool] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=30.0,
            )
        return self._client

    async def _get_direct_client(self) -> httpx.AsyncClient:
        """Get or create direct HTTP client (no base URL)."""
        if self._direct_client is None or self._direct_client.is_closed:
            self._direct_client = httpx.AsyncClient(timeout=30.0)
        return self._direct_client

    async def close(self) -> None:
        """Close the HTTP clients."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
        if self._direct_client and not self._direct_client.is_closed:
            await self._direct_client.aclose()

    async def health_check(self) -> bool:
        """Check if Dapr sidecar is healthy."""
        try:
            client = await self._get_client()
            response = await client.get("/v1.0/healthz")
            self._dapr_available = response.status_code == 204
            return self._dapr_available
        except Exception as e:
            logger.warning(f"Dapr health check failed: {e}")
            self._dapr_available = False
            return False

    async def invoke_service(
        self,
        app_id: str,
        method: str,
        data: Optional[dict[str, Any]] = None,
        http_verb: str = "POST",
    ) -> dict[str, Any]:
        """Invoke another service via Dapr or direct HTTP fallback."""
        # Try Dapr first if available
        if self._dapr_available is not False:
            try:
                client = await self._get_client()
                url = f"/v1.0/invoke/{app_id}/method/{method}"
                if http_verb.upper() == "GET":
                    response = await client.get(url)
                else:
                    response = await client.request(
                        method=http_verb.upper(),
                        url=url,
                        json=data,
                    )
                response.raise_for_status()
                self._dapr_available = True
                return response.json()
            except Exception as e:
                logger.info(f"Dapr invocation failed, trying direct: {e}")
                self._dapr_available = False

        # Fallback: direct HTTP call to service
        base_url = self.DIRECT_SERVICE_MAP.get(app_id)
        if not base_url:
            raise Exception(f"No direct URL for service: {app_id}")

        client = await self._get_direct_client()
        url = f"{base_url}/{method}"
        logger.info(f"Direct service call: {http_verb} {url}")

        if http_verb.upper() == "GET":
            response = await client.get(url)
        else:
            response = await client.request(
                method=http_verb.upper(),
                url=url,
                json=data,
            )

        response.raise_for_status()
        return response.json()


# Global client instance
_dapr_client: Optional[DaprClient] = None


def get_dapr_client() -> DaprClient:
    """Get the global Dapr client instance."""
    global _dapr_client
    if _dapr_client is None:
        _dapr_client = DaprClient()
    return _dapr_client


# Re-export utilities
from .pubsub import publish_event, subscribe_handler
from .state import delete_state, get_state, save_state

__all__ = [
    "DaprClient",
    "get_dapr_client",
    "publish_event",
    "subscribe_handler",
    "get_state",
    "save_state",
    "delete_state",
]
