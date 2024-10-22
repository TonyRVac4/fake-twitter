from typing import List, Optional, Dict

from sqlalchemy import select, delete, update
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncSession
from db_config import BaseModel, base_metadata, intpk


class Tweets(BaseModel):
    __tablename__ = "tweets"
    metadata = base_metadata

    id: intpk
    user_id: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[str] = mapped_column(nullable=False)  # изменить тип и ограничить длину


class Medias(BaseModel):
    __tablename__ = "medias"
    metadata = base_metadata

    id: intpk
    tweet_id: Mapped[int] = mapped_column(nullable=False)
    data: Mapped[str] = mapped_column(nullable=False)  # изменить тип и ограничить длину


class Likes(BaseModel):
    __tablename__ = "likes"
    metadata = base_metadata

    id: intpk
    user_id: Mapped[int] = mapped_column(nullable=False)
    tweet_id: Mapped[int] = mapped_column(nullable=False)
