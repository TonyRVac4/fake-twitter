from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from src.main import app

client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Async Fixture yields async client for testing the app.

    Yields:
        AsyncClient
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test", timeout=2,
    ) as async_client:
        yield async_client
