"""
Shared test fixtures for LearnFlow backend integration tests.
"""

import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient

# Add backend root to path so services can import shared
backend_root = str(Path(__file__).parent.parent)
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)


@pytest.fixture
def student_id():
    return uuid4()


@pytest.fixture
def session_id():
    return uuid4()


@pytest.fixture
def mock_dapr_client():
    """Mock Dapr client for tests that don't need real infrastructure."""
    client = AsyncMock()
    client.health_check = AsyncMock(return_value=True)
    client.invoke_service = AsyncMock(return_value={})
    client.publish_event = AsyncMock()
    client.get_state = AsyncMock(return_value=None)
    client.save_state = AsyncMock()
    client.close = AsyncMock()
    return client


@pytest.fixture
def mock_publish_event():
    """Mock for shared.dapr.publish_event."""
    return AsyncMock()
