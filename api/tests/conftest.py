import time
from subprocess import run  # noqa
from typing import AsyncGenerator

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker  # noqa
from sqlalchemy.pool import NullPool
from types_aiobotocore_s3 import Client  # noqa
from src.config import DATABASE_URL, S3_ACCESS_KEY, S3_SECRET_KEY, S3_URL, S3_BUCKET_NANE  # noqa
from src.database_models.db_config import base_metadata, get_async_session  # noqa
from src.utils.s3_config import S3Client, get_async_s3_client  # noqa
from src.main import app  # noqa
from src.migrations.run_migration import apply_head_migration  # noqa
from tests.db_setup import setup_test_data  # noqa

test_engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
test_async_session = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async Generator yields async session for api testing.

    Yields:
        AsyncSession
    """
    async with test_async_session() as session:
        yield session


async def override_s3_client() -> AsyncGenerator[Client, None]:
    """Async Generator yields async client for s3 storage testing.

    Yields:
        Client: async s3 client
    """
    s3_client = S3Client(
        access_key=S3_ACCESS_KEY,
        secret_key=S3_SECRET_KEY,
        endpoint_url=S3_URL,
        bucket_name=S3_BUCKET_NANE,
    )
    yield s3_client


app.dependency_overrides[get_async_session] = override_async_session
app.dependency_overrides[get_async_s3_client] = override_s3_client


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
async def s3_ac() -> AsyncGenerator[Client, None]:
    """Async fixture: yield async session for testing the db.

    Yields:
        AsyncSession
    """
    yield override_s3_client()


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Async fixture: yield async client for testing the app.

    Yields:
        AsyncClient
    """
    async with LifespanManager(app):
        async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
            timeout=2,
        ) as async_client:
            yield async_client
