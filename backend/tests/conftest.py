"""Root conftest — shared fixtures for all unit tests (Polsia pattern)."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture(autouse=True)
def mock_claude_cli(monkeypatch):
    """Prevent any real claude CLI calls in unit tests."""
    monkeypatch.setenv("CLAUDE_CLI_MOCK", "true")
    monkeypatch.setenv(
        "CLAUDE_CLI_MOCK_RESPONSE",
        json.dumps({"result": "Mock Claude response for testing"}),
    )


@pytest.fixture
def mock_redis(mocker):
    mock = AsyncMock()
    mock.publish = AsyncMock(return_value=1)
    mocker.patch("app.core.redis_client.get_redis", return_value=mock)
    return mock


@pytest.fixture
def mock_chroma(mocker):
    collection = MagicMock()
    collection.add = MagicMock()
    collection.query = MagicMock(return_value={
        "documents": [["Mock memory content"]],
        "metadatas": [[{"category": "strategy", "title": "Test", "source": "test"}]],
        "ids": [["mock-id-1"]],
        "distances": [[0.1]],
    })
    mocker.patch("app.core.chroma_client.get_collection", return_value=collection)
    mocker.patch("app.services.memory_service.get_collection", return_value=collection)
    return collection
