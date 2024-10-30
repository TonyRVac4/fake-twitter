from typing import List, Dict, Any

from sqlalchemy import select, delete, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database_models.users_orm_models import Users, Followers, Cookies
from database_models.tweets_orm_models import Tweets, Medias, Likes
from database_models.db_config import BaseModel, base_metadata, engine, async_session, ResponseData


class TweetsMethods(Tweets):
    @classmethod
    async def get_all(cls, user_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            expression = select(Tweets).where(Tweets.user_id == user_id)
            # изменить с твитов самого пользователя на ленту для него и переименовать сам метод
            request = await session.execute(expression)
            request_data: list = request.scalars().fetchall()

            if request_data:
                result: dict = {"result": True, "tweet": []}
                code: int = 200

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
            else:
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "User with id:{id} not found".format(id=user_id),
                }, 404

            return ResponseData(response=result, status_code=code)

    @classmethod
    async def add(cls, user_id: int, data: dict, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            new_tweet = Tweets(user_id=user_id, data=data["tweet_data"])
            session.add(new_tweet)
            await session.commit()
            return ResponseData(response={"result": True, "tweet_id": new_tweet.id}, status_code=201)

    @classmethod
    async def delete(cls, user_id: int, tweet_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            check_tweet_exists_exp = select(Tweets).where(Tweets.id == tweet_id)
            check_request = await session.execute(check_tweet_exists_exp)
            check_result = check_request.scalars().one_or_none()

            if check_result:
                if check_result.user_id == user_id:
                    del_expr = delete(Tweets).where(and_(Tweets.id == tweet_id, user_id == user_id))
                    await session.execute(del_expr)
                    await session.commit()
                    result, code = {"result": True}, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "ActionForbidden",
                        "error_message": "You can not delete other people's tweets!",
                    }, 401
            else:
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "Tweet with id:{id} not found".format(id=tweet_id),
                }, 404

            return ResponseData(response=result, status_code=code)
