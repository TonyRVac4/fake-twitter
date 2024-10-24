from typing import List, Optional, Dict
from datetime import datetime, timedelta

from sqlalchemy import select, delete
from sqlalchemy.types import VARCHAR, DATETIME
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession

from db_config import BaseModel, base_metadata


class Users(BaseModel):
    __tablename__ = "users"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(15), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(VARCHAR(30), unique=True, nullable=False)

    @classmethod
    async def basic_template(cls, session: AsyncSession) -> Dict:
        async with session as session:
             data = await session.get()
        return ...


class Followers(BaseModel):
    __tablename__ = "followers"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    follower_id: Mapped[int] = mapped_column(nullable=False)


class Cookies(BaseModel):
    __tablename__ = "cookies"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    hash: Mapped[str] = mapped_column(VARCHAR(100), unique=True, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(
        DATETIME,
        nullable=False,
        default=datetime.now() + timedelta(7),
    )
