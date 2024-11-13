from typing import AsyncGenerator

from sqlalchemy import MetaData, NullPool
from sqlalchemy.ext.asyncio import create_async_engine  # noqa
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker  # noqa
from sqlalchemy.orm import declarative_base  # noqa
from config import DATABASE_URL  # noqa

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

base_metadata = MetaData()
BaseModel = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async generator yields main async session for api.

    Yields:
        AsyncGenerator
    """
    async with async_session() as session:
        yield session


class ResponseData:
    """Class for returning results from orm methods."""

    def __init__(self, response: dict, status_code: int):
        """Init.

        Parameters:
            response: dict
            status_code: int
        """
        self.response = response
        self.status_code = status_code
