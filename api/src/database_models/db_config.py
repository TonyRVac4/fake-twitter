from typing import AsyncGenerator, Annotated

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, mapped_column, Mapped
from sqlalchemy import NullPool, MetaData

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session = async_sessionmaker(engine, expire_on_commit=False)

base_metadata = MetaData()
BaseModel = declarative_base()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Async generator yields main async session for api"""

    async with async_session() as session:
        yield session
