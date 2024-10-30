from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import NullPool, MetaData

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = async_sessionmaker(engine, expire_on_commit=False, autoflush=True)

base_metadata = MetaData()
BaseModel = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async generator yields main async session for api"""

    async with async_session() as session:
        yield session


class ResponseData:
    def __init__(self, response: dict, status_code: int):
        self.response = response
        self.status_code = status_code
