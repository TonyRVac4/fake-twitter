import os.path
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool

from src.main import app
from src.config import DATABASE_URL as DATABASE_URL_TEST  # configure test db
from src.database_models.db_config import get_async_session, base_metadata

client = TestClient(app)


test_engin = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
test_async_session = async_sessionmaker(test_engin, expire_on_commit=False)
base_metadata.bind = test_engin


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async Generator yields async session for api testing."""
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_async_session


@pytest.fixture(autouse=True, scope="session")
async def set_up_db() -> None:
    """
    Async Fixture creates the tables in the test database
    and drops them after tests.
    """
    async with test_engin.begin() as conn:
        await conn.run_sync(base_metadata.create_all)
        yield
        await conn.run_sync(base_metadata.drop_all)

    # if os.path.exists(abs_path_to_test_db):
    #     os.remove(abs_path_to_test_db)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Async Fixture yields async client for testing the app.

    Yields:
        AsyncClient
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=2,
    ) as async_client:
        yield async_client
