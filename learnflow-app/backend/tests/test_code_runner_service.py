"""
Integration tests for the Code Runner Service.

Tests sandboxed code execution and struggle detection.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "services" / "code-runner"))


@pytest.fixture
def mock_dependencies():
    """Mock external dependencies for code-runner service."""
    with (
        patch("shared.dapr.get_dapr_client") as mock_dapr_factory,
        patch("shared.dapr.publish_event", new_callable=AsyncMock) as mock_publish,
        patch("shared.dapr.get_state", new_callable=AsyncMock) as mock_get_state,
        patch("shared.dapr.save_state", new_callable=AsyncMock) as mock_save_state,
    ):
        mock_dapr = AsyncMock()
        mock_dapr.health_check = AsyncMock(return_value=True)
        mock_dapr.close = AsyncMock()
        mock_dapr_factory.return_value = mock_dapr

        mock_get_state.return_value = None

        yield {
            "dapr": mock_dapr,
            "publish": mock_publish,
        }


@pytest.fixture
async def runner_client(mock_dependencies):
    """Create async test client for code-runner service."""
    from services.code_runner.main import app  # noqa: may need adjustment

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_health_check(runner_client):
    """Health endpoint returns service status."""
    response = await runner_client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == "code-runner"


@pytest.mark.asyncio
async def test_execute_valid_code(runner_client, student_id, mock_dependencies):
    """Successful code execution returns stdout."""
    response = await runner_client.post(
        "/api/v1/code/execute",
        json={
            "student_id": str(student_id),
            "code": "print('hello world')",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["exit_code"] == 0
    assert "hello world" in data["stdout"]
    assert data["timed_out"] is False

    # Verify result event published
    mock_dependencies["publish"].assert_called()


@pytest.mark.asyncio
async def test_execute_syntax_error(runner_client, student_id):
    """Code with syntax errors returns non-zero exit code."""
    response = await runner_client.post(
        "/api/v1/code/execute",
        json={
            "student_id": str(student_id),
            "code": "def foo(\n  bar",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["exit_code"] != 0
    assert data["stderr"] != ""


@pytest.mark.asyncio
async def test_execute_empty_code_rejected(runner_client, student_id):
    """Empty code should be rejected by validation."""
    response = await runner_client.post(
        "/api/v1/code/execute",
        json={
            "student_id": str(student_id),
            "code": "",
        },
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_execute_runtime_error(runner_client, student_id):
    """Runtime errors return stderr with error info."""
    response = await runner_client.post(
        "/api/v1/code/execute",
        json={
            "student_id": str(student_id),
            "code": "x = 1 / 0",
        },
    )
    assert response.status_code == 200

    data = response.json()
    assert data["exit_code"] != 0
    assert "ZeroDivisionError" in data["stderr"]
