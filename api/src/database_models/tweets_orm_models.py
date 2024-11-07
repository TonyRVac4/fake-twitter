from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.types import VARCHAR
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database_models.db_config import BaseModel, base_metadata  # noqa


class Tweets(BaseModel):
    __tablename__ = "tweets"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True,)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    data: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)

    medias: Mapped[List["Medias"]] = relationship(back_populates="tweet", uselist=True, lazy="selectin")
    user: Mapped["Users"] = relationship(back_populates="tweets", uselist=True, lazy="selectin")
    likes: Mapped[List["Likes"]] = relationship(back_populates="tweet", uselist=True, lazy="selectin", cascade="all, delete-orphan")


class Medias(BaseModel):
    __tablename__ = "medias"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE",), nullable=False)
    data: Mapped[str] = mapped_column(nullable=False)  # непонятно как хранить медиа

    tweet: Mapped["Tweets"] = relationship(back_populates="medias")


class Likes(BaseModel):
    __tablename__ = "likes"
    metadata = base_metadata

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE",), nullable=False, primary_key=True)
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE",), nullable=False, primary_key=True)

    user: Mapped["Users"] = relationship(back_populates="likes", lazy="selectin")
    tweet: Mapped["Tweets"] = relationship(back_populates="likes", lazy="selectin")

    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="unique_like"),)
