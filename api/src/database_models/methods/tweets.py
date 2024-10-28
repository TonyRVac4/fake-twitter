from typing import List, Dict, Any

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database_models.users_orm_models import Users, Followers, Cookies
from database_models.tweets_orm_models import Tweets, Medias, Likes
from database_models.db_config import BaseModel, base_metadata, engine, async_session


class TweetsMethods(Tweets):
    @classmethod
    async def get_all(cls, async_session: AsyncSession, user_id) -> dict:
        async with async_session as session:
            expression = select(Tweets).where(Tweets.user_id == user_id)
            request = await session.execute(expression)

            result: dict = {"result": True, "tweet": []}

            for res in request.scalars().fetchall():
                author: dict = {"id": res.user.id, "name": res.user.username}
                attachments: List[str] = [media.data for media in res.medias]
                likes: List[dict] = [{"user_id": like.user_id, "name": like.user.username} for like in res.likes]

                result["tweet"].append(
                    {
                        "id": res.id,
                        "content": res.data,
                        "attachments": attachments,
                        "author": author,
                        "likes": likes
                    }
                )
            return result
