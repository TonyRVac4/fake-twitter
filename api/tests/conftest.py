import time
from subprocess import run  # noqa
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker  # noqa
from sqlalchemy.pool import NullPool
from src.config import DATABASE_URL
from src.database_models.db_config import base_metadata, get_async_session
from src.main import app
from src.migrations.run_migration import apply_head_migration
from tests.db_setup import setup_test_data

test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async Generator yields async session for api testing.

    Yields:
        AsyncSession
    """
    async with test_async_session() as session:
        yield session


app.dependency_overrides[get_async_session] = override_async_session


@pytest.fixture(scope="session", autouse=True)
def create_postgresql_db() -> None:
    """Sync fixture.

    Create all tables using head alembic migration.

    Yields:
        None
    """
    time.sleep(2)
    apply_head_migration()
    time.sleep(2)
    yield


@pytest.fixture(scope="session", autouse=True)
async def set_up_test_data(create_postgresql_db) -> None:  # noqa
    """Async fixture.

    Fill the test database with data
    and download the additional extension for PostgreSQL.

    Parameters:
        create_postgresql_db: fixture that creates db

    Yields:
        None
    """
    async with test_engine.connect() as con:
        await con.run_sync(base_metadata.create_all)
        await con.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
        await con.commit()

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
