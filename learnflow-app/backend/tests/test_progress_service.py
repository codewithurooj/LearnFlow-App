"""
Integration tests for the Progress Service.

Tests mastery calculation, progress retrieval, and event handling.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / "services" / "progress"))


@pytest.fixture
def mock_dependencies():
    """Mock external dependencies for progress service."""
    with (
        patch("shared.dapr.get_dapr_client") as mock_dapr_factory,
        patch("shared.dapr.publish_event", new_callable=AsyncMock) as mock_publish,
    ):
        mock_dapr = AsyncMock()
        mock_dapr.health_check = AsyncMock(return_value=True)
        mock_dapr.close = AsyncMock()
        mock_dapr_factory.return_value = mock_dapr

        yield {
            "dapr": mock_dapr,
            "publish": mock_publish,
        }


@pytest.fixture
def mock_student_progress():
    """Mock get_student_progress to return sample data."""
    from datetime import datetime

    sample_state = AsyncMock()
    sample_state.topics = {
        "variables": {
            "topic_name": "Variables",
            "exercises_score": 0.8,
            "quizzes_score": 0.7,
            "code_quality_score": 0.9,
            "streak_bonus": 0.5,
            "exercises_completed": 5,
            "quizzes_taken": 3,
            "total_score": 0.77,
            "level": "Proficient",
            "level_color": "green",
            "last_activity": datetime.now().isoformat(),
        },
        "loops": {
            "topic_name": "Loops",
            "exercises_score": 0.4,
            "quizzes_score": 0.3,
            "code_quality_score": 0.5,
            "streak_bonus": 0.2,
            "exercises_completed": 2,
            "quizzes_taken": 1,
            "total_score": 0.38,
            "level": "Beginner",
            "level_color": "red",
            "last_activity": datetime.now().isoformat(),
        },
    }
    sample_state.current_streak = 3
    sample_state.updated_at = datetime.now().isoformat()

    return sample_state


@pytest.fixture
async def progress_client(mock_dependencies, mock_student_progress):
    """Create async test client for progress service."""
    with patch("events.get_student_progress", return_value=mock_student_progress):
        from services.progress.main import app

        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            yield client


@pytest.mark.asyncio
async def test_health_check(progress_client):
    """Health endpoint returns service status."""
    response = await progress_client.get("/api/v1/health")
    assert response.status_code == 200

    data = response.json()
    assert data["service"] == "progress"


@pytest.mark.asyncio
async def test_get_progress_summary(progress_client, student_id):
    """Returns overall progress with topic summaries."""
    response = await progress_client.get(f"/api/v1/progress/{student_id}")
    assert response.status_code == 200

    data = response.json()
    assert "overall_mastery" in data
    assert "topics" in data
    assert len(data["topics"]) == 2
    assert data["current_streak"] == 3


@pytest.mark.asyncio
async def test_get_topic_progress(progress_client, student_id):
    """Returns detailed progress for a specific topic."""
    response = await progress_client.get(
        f"/api/v1/progress/{student_id}/topic/variables"
    )
    assert response.status_code == 200

    data = response.json()
    assert data["topic_name"] == "Variables"
    assert "breakdown" in data
    assert "improvement_suggestions" in data


@pytest.mark.asyncio
async def test_get_topic_not_found(progress_client, student_id):
    """Requesting unknown topic returns 404."""
    response = await progress_client.get(
        f"/api/v1/progress/{student_id}/topic/nonexistent"
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_topics_grouped_by_level(progress_client, student_id):
    """Topics are grouped by mastery level."""
    response = await progress_client.get(
        f"/api/v1/progress/{student_id}/topics"
    )
    assert response.status_code == 200

    data = response.json()
    assert "Proficient" in data
    assert "Beginner" in data
