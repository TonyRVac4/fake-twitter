from typing import List, Optional, Dict

from sqlalchemy import select, delete
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from db_config import BaseModel, base_metadata, intpk


class Users(BaseModel):
    __tablename__ = "users"
    metadata = base_metadata

    id: intpk
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    # password: Mapped[str] = mapped_column() разобраться с хранением!

    @classmethod
    async def basic_template(cls, session: AsyncSession) -> Dict:
        async with session as session:
             data = await session.get()
        return ...


class Followers(BaseModel):
    __tablename__ = "followers"
    metadata = base_metadata

    id: intpk
    user_id: Mapped[int] = mapped_column(nullable=False)
    follower_id: Mapped[int] = mapped_column(nullable=False)


class Cookies(BaseModel):
    __tablename__ = "cookies"
    metadata = base_metadata

    id: intpk
    user_id: Mapped[int] = mapped_column(nullable=False)
    # hash: Mapped[str] = mapped_column() разобраться с хранением!
