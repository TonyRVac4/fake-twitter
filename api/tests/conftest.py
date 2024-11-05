import os.path
import time
import shutil
from typing import AsyncGenerator
from subprocess import run

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from src.main import app  # noqa
from src.config import DATABASE_URL  # noqa
from src.migrations.run_migration import apply_head_migration  # noqa
from src.database_models.db_config import get_async_session, base_metadata  # noqa
from tests.db_setup import setup_test_data  # noqa

path_to_dir = os.path.dirname(os.path.abspath(__file__))

test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async Generator yields async session for api testing."""
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_async_session


@pytest.fixture(scope="session", autouse=True)
def set_up_postgresql_db() -> None:
    """
    Sync fixture: create and remove docker container with test PostgreSQL db
    and create all tables using head alembic migration.
    """
    path_to_docker_compose = path_to_dir + "/docker-compose.yaml"
    run(["docker-compose", "-f", path_to_docker_compose, "up", "-d"])
    time.sleep(5)
    try:
        apply_head_migration()
        time.sleep(2)
        yield
    finally:
        run(["docker-compose", "-f", path_to_docker_compose, "rm", "-sf"])
        if os.path.exists(path_to_dir + "/test_db"):
            shutil.rmtree(path_to_dir + "/test_db")


@pytest.fixture(scope="session", autouse=True)
async def set_up_test_data(set_up_postgresql_db) -> None:
    """
    Async fixture: fill the test database with data
    and download the additional extension for PostgreSQL.
    """
    async with test_engine.connect() as conn:
        await conn.run_sync(base_metadata.create_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
        await conn.commit()

        async with test_async_session() as session:
            await setup_test_data(session)

        yield

    async with test_engine.begin() as conn:
        await conn.run_sync(base_metadata.drop_all)


@pytest.fixture(scope="session")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async fixture: yield async session for testing the db.

    Yields:
        AsyncSession
    """
    async with test_async_session() as session:
        yield session


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Async fixture: yield async client for testing the app.

    Yields:
        AsyncClient
    """
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
        timeout=2,
    ) as async_client:
        yield async_client
