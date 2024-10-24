from typing import List, Optional, Dict

from sqlalchemy import select, delete, update
from sqlalchemy.types import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession

from db_config import BaseModel, base_metadata


class Tweets(BaseModel):
    __tablename__ = "tweets"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)


class Medias(BaseModel):
    __tablename__ = "medias"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[str] = mapped_column(nullable=False)  # непонятно как хранить медиа


class Likes(BaseModel):
    __tablename__ = "likes"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[int] = mapped_column(nullable=False)
    tweet_id: Mapped[int] = mapped_column(nullable=False)
