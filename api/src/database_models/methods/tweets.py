from typing import List, Dict, Any

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from database_models.users_orm_models import Users, Followers, Cookies
from database_models.tweets_orm_models import Tweets, Medias, Likes
from database_models.db_config import BaseModel, base_metadata, engine, async_session


class TweetsMethods(Tweets):
    @classmethod
    async def get_all(cls, user_id, async_session: AsyncSession) -> dict:
        async with async_session as session:
            expression = select(Tweets).where(Tweets.user_id == user_id)

            request = await session.execute(expression)
            request_data: list = request.scalars().fetchall()

            if not request_data:
                return {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "User with id:{id} not found".format(id=user_id),
                }

            result: dict = {"result": True, "tweet": []}

            for res in request_data:
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
