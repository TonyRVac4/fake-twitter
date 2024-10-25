import asyncio
from typing import List

from sqlalchemy import select, delete, update, ForeignKey, UniqueConstraint
from sqlalchemy.types import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from database_models.users_models import Users
from db_config import BaseModel, base_metadata, engine, async_session


class Tweets(BaseModel):
    __tablename__ = "tweets"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True,)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    data: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)

    medias: Mapped[List["Medias"]] = relationship(back_populates="tweet", uselist=True, lazy="joined")
    user: Mapped["Users"] = relationship(back_populates="tweets")


class Medias(BaseModel):
    __tablename__ = "medias"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id",), nullable=False)
    data: Mapped[str] = mapped_column(nullable=False)  # непонятно как хранить медиа

    tweet: Mapped["Tweets"] = relationship(back_populates="medias")


class Likes(BaseModel):
    __tablename__ = "likes"
    metadata = base_metadata

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=False, primary_key=True)

    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="unique_like"),)
