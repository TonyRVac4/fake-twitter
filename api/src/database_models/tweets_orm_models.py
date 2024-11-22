from typing import List

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import VARCHAR
from database_models.db_config import BaseModel, base_metadata  # noqa


class Tweets(BaseModel):
    """Sqlalchemy table class.

    __tablename__: tweets

    id (int): ID (primary_key, autoincrement)
    user_id (int): id of the tweet author (ForeignKey)
    data (str): Tweet's text. (limit 1000)
    """

    __tablename__ = "tweets"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    data: Mapped[str] = mapped_column(VARCHAR(1000), nullable=False)

    medias: Mapped[List["Medias"]] = relationship(
        back_populates="tweet", uselist=True, lazy="selectin",
    )
    user: Mapped["Users"] = relationship(
        back_populates="tweets", uselist=True, lazy="selectin",
    )
    likes: Mapped[List["Likes"]] = relationship(
        back_populates="tweet",
        uselist=True,
        lazy="selectin",
        cascade="all, delete-orphan",
    )


class Medias(BaseModel):
    """Sqlalchemy table class.

    __tablename__: medias

    id (int): ID (primary_key, autoincrement)
    tweet_id (int): id of the tweet (ForeignKey)
    data (str): no idea
    """

    __tablename__ = "medias"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(
        primary_key=True, nullable=False, autoincrement=True,
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tweets.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    link: Mapped[str] = mapped_column(VARCHAR(150), nullable=False)

    tweet: Mapped["Tweets"] = relationship(back_populates="medias")


class Likes(BaseModel):
    """Sqlalchemy table class.

    __tablename__: likes

    tweet_id (int): id of the user who liked (ForeignKey)
    tweet_id (int): id of the tweet (ForeignKey)
    """

    __tablename__ = "likes"
    metadata = base_metadata

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        primary_key=True,
    )
    tweet_id: Mapped[int] = mapped_column(
        ForeignKey(
            "tweets.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        primary_key=True,
    )

    user: Mapped["Users"] = relationship(back_populates="likes", lazy="selectin")
    tweet: Mapped["Tweets"] = relationship(back_populates="likes", lazy="selectin")

    __table_args__ = (UniqueConstraint("user_id", "tweet_id", name="unique_like"),)
