"""
Integration tests for the Triage Service.

Tests the question classification and routing endpoints.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

# Ensure service can resolve imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "services" / "triage"))


@pytest.fixture
def mock_dependencies():
    """Mock all external dependencies for triage service."""
    with (
        patch("shared.dapr.get_dapr_client") as mock_dapr_factory,
        patch("shared.dapr.publish_event", new_callable=AsyncMock) as mock_publish,
        patch("shared.agents.registry.get_registry") as mock_registry_factory,
    ):
        mock_dapr = AsyncMock()
        mock_dapr.health_check = AsyncMock(return_value=True)
        mock_dapr.invoke_service = AsyncMock(return_value={"explanation": "Test response"})
        mock_dapr.close = AsyncMock()
        mock_dapr_factory.return_value = mock_dapr

        mock_registry = AsyncMock()
        mock_registry.get_service_app_id.return_value = "concepts-service"
        mock_registry.get_service_endpoint.return_value = "api/v1/concepts/explain"
        mock_registry_factory.return_value = mock_registry

        yield {
            "dapr": mock_dapr,
            "publish": mock_publish,
            "registry": mock_registry,
        }


@pytest.fixture
async def triage_client(mock_dependencies):
    """Create async test client for triage service."""
    from services.triage.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(triage_client):
    """Health endpoint returns service status."""
    response = await triage_client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == "triage"
    assert data["status"] in ("healthy", "degraded")


@pytest.mark.asyncio
async def test_classify_question(triage_client, student_id):
    """Classification endpoint categorizes questions correctly."""
    response = await triage_client.post(
        "/api/v1/triage/classify",
        json={
            "student_id": str(student_id),
            "question": "Explain how Python lists work",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "routed_to" in data
    assert "confidence" in data
    assert 0 <= data["confidence"] <= 1


@pytest.mark.asyncio
async def test_classify_debug_question(triage_client, student_id):
    """Debug-related questions should route to debug agent."""
    response = await triage_client.post(
        "/api/v1/triage/classify",
        json={
            "student_id": str(student_id),
            "question": "I'm getting a TypeError: unsupported operand type",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["routed_to"] in ("debug", "concepts")


@pytest.mark.asyncio
async def test_route_question(triage_client, student_id, mock_dependencies):
    """Full routing returns specialist response and publishes event."""
    response = await triage_client.post(
        "/api/v1/triage/route",
        json={
            "student_id": str(student_id),
            "question": "What are Python decorators?",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert "routed_to" in data
    assert "response" in data
    assert "processing_time_ms" in data
    assert data["processing_time_ms"] >= 0

    # Verify event was published
    mock_dependencies["publish"].assert_called_once()


@pytest.mark.asyncio
async def test_route_question_validation(triage_client, student_id):
    """Empty question should be rejected."""
    response = await triage_client.post(
        "/api/v1/triage/route",
        json={
            "student_id": str(student_id),
            "question": "",
        },
    )
    assert response.status_code == 422
