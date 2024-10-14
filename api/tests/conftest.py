from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

from src.main import app


client = TestClient(app)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Async Fixture yields async client for testing the app

    """

    async with AsyncClient(transport=ASGITransport(app=app),  base_url="http://test") as ac:
        yield ac
