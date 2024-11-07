from typing import List

from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from database_models.users_orm_models import Users, Followers, Cookies  # noqa
from database_models.tweets_orm_models import Tweets, Medias, Likes  # noqa
from database_models.db_config import BaseModel, base_metadata, engine, async_session, ResponseData  # noqa


class TweetsMethods(Tweets):
    @classmethod
    async def get_posts_for_user(cls, user_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            get_user_expr = select(Followers).where(Followers.follower_id == user_id).options(
                selectinload(Followers.user).selectinload(Users.tweets).selectinload(Tweets.likes).selectinload(Likes.user)
            )
            request = await session.execute(get_user_expr)
            follows: list = request.scalars().fetchall()

            result: dict = {"result": True, "tweet": []}
            code: int = 200

            if follows:
                for follow in follows:
                    author_info: dict = {"id": follow.user.id, "name": follow.user.username}

                    for tweet in follow.user.tweets:
                        attachments: List[str] = [media.data for media in tweet.medias]
                        likes: List[dict] = [{"user_id": like.user_id, "name": like.user.username} for like in tweet.likes]

                        result["tweet"].append(
                            {
                                "id": tweet.id,
                                "content": tweet.data,
                                "attachments": attachments,
                                "author": author_info,
                                "likes": likes
                            }
                        )

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
                    del_expr = delete(Tweets).where(Tweets.id == tweet_id)
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
                    "error_message": "Tweet doesn't exist.",
                }, 404

            return ResponseData(response=result, status_code=code)


class LikesMethods(Likes):
    @classmethod
    async def add(cls, user_id: int, tweet_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            try:
                new_like = Likes(user_id=user_id, tweet_id=tweet_id)
                session.add(new_like)
                await session.commit()
                result, code = {"result": True}, 201
            except IntegrityError:
                result, code = {
                    "result": False,
                    "error_type": "UniqueViolationError",
                    "error_message": "Like already exists.",
                }, 400

            return ResponseData(response=result, status_code=code)

    @classmethod
    async def delete(cls, user_id: int, tweet_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            check_like_exists_exp = select(Likes).where(and_(Likes.user_id == user_id, Likes.tweet_id == tweet_id))
            check_request = await session.execute(check_like_exists_exp)
            check_result = check_request.scalars().one_or_none()

            if check_result:
                expression = delete(Likes).where(and_(Likes.user_id == user_id, Likes.tweet_id == tweet_id))
                await session.execute(expression)
                await session.commit()
                result, code = {"result": True}, 200
            else:
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "Like doesn't exist.",
                }, 404
            return ResponseData(response=result, status_code=code)
