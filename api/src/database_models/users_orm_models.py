from typing import List
from datetime import datetime, timedelta

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.types import VARCHAR, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped, relationship

from database_models.db_config import BaseModel, base_metadata


class Users(BaseModel):
    __tablename__ = "users"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True,)
    username: Mapped[str] = mapped_column(VARCHAR(15), unique=True, nullable=False,)
    email: Mapped[str] = mapped_column(VARCHAR(30), unique=True, nullable=False,)

    tweets: Mapped[List["Tweets"]] = relationship(back_populates="user", uselist=True, lazy="selectin")

    followers: Mapped[List["Followers"]] = relationship(back_populates="user",
                                                        foreign_keys='Followers.user_id',
                                                        uselist=True,

                                                        )
    following: Mapped[List["Followers"]] = relationship(back_populates="follower",
                                                        foreign_keys='Followers.follower_id',
                                                        uselist=True,

                                                        )

    likes: Mapped[List["Likes"]] = relationship(back_populates="user", uselist=True)


class Followers(BaseModel):
    __tablename__ = "followers"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False,)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False,)
    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False,)

    user: Mapped["Users"] = relationship(foreign_keys=[user_id],
                                         back_populates='followers',
                                         )
    follower: Mapped["Users"] = relationship(foreign_keys=[follower_id],
                                             back_populates='following',
                                             )

    __table_args__ = (UniqueConstraint("user_id",
                                       "follower_id",
                                       name="unique_follow",
                                       ),
                      )


class Cookies(BaseModel):
    __tablename__ = "cookies"
    metadata = base_metadata

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True,)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    hash: Mapped[str] = mapped_column(VARCHAR(100), unique=True, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(
        TIMESTAMP,
        nullable=False,
        default=datetime.now() + timedelta(7),
    )
