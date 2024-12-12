from sqlalchemy import and_, delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from database_models.db_config import ResponseData  # noqa
from database_models.tweets_orm_models import Likes, MediasTweets, Medias, Tweets  # noqa
from database_models.users_orm_models import Cookies, Followers, Users  # noqa
from utils.logger_config import orm_logger  # noqa


class TweetsMethods(Tweets):
    """Class with Orm methods for Tweets table."""

    @classmethod
    async def get(
        cls, tweet_id: int, async_session: AsyncSession,
    ) -> ResponseData:
        """Return tweet by id.

        Parameters:
            tweet_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                expr = select(Tweets).where(Tweets.id == tweet_id)
                request = await session.execute(expr)
                tweet = request.scalars().one_or_none()
                if tweet:
                    result, code = {"result": True, "tweet": tweet}, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "DataNotFound",
                        "error_message": "Tweet does not exist",
                    }, 404
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)

    @classmethod
    async def get_posts_list(
        cls, user_id: int, async_session: AsyncSession,
    ) -> ResponseData:
        """Return posts from followed pages for user by id.

        Parameters:
            user_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                get_follows_expr = (
                    select(Followers).
                    where(Followers.follower_id == user_id).
                    options(
                        selectinload(Followers.user).
                        selectinload(Users.tweets).
                        selectinload(Tweets.likes).
                        selectinload(Likes.user),
                    )
                )
                get_users_posts = select(Tweets).where(Tweets.user_id == user_id)
                get_follows_request = await session.execute(get_follows_expr)
                get_users_posts_request = await session.execute(get_users_posts)
                follows: list = get_follows_request.scalars().fetchall()
                users_posts: list = get_users_posts_request.scalars().fetchall()

                tweets: list = []

                if follows:
                    for follow in follows:
                        for tweet in follow.user.tweets:
                            tweets.append(
                                {
                                    "id": tweet.id,
                                    "content": tweet.data,
                                    "attachments": [
                                        media.link for media in tweet.medias
                                    ],
                                    "author": {
                                        "id": tweet.user.id,
                                        "name": tweet.user.username,
                                    },
                                    "likes": [
                                        {
                                            "user_id": like.user_id,
                                            "name": like.user.username,
                                        }
                                        for like in tweet.likes
                                    ],
                                },
                            )
                if users_posts:
                    for user_tweet in users_posts:
                        tweets.append(
                            {
                                "id": user_tweet.id,
                                "content": user_tweet.data,
                                "attachments": [
                                    media.link for media in user_tweet.medias
                                ],
                                "author": {
                                    "id": user_tweet.user.id,
                                    "name": user_tweet.user.username,
                                },
                                "likes": [
                                    {
                                        "user_id": like.user_id,
                                        "name": like.user.username,
                                    }
                                    for like in user_tweet.likes
                                ],
                            },
                        )

                sorted_tweets = sorted(
                    tweets, key=lambda i_tweet: len(i_tweet["likes"]), reverse=True,
                )
                result, code = {"result": True, "tweets": sorted_tweets}, 200
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)

    @classmethod
    async def add(
        cls,
        user_id: int,
        data: dict,
        async_session: AsyncSession,
    ) -> ResponseData:
        """Add tweet to tweets table.

        Parameters:
            user_id: int
            data: {"tweet_data": str, "tweet_media_ids": Array[int]}
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                new_tweet = Tweets(user_id=user_id, data=data["tweet_data"])
                session.add(new_tweet)
                await session.flush()

                if data["tweet_media_ids"]:
                    for m_id in data["tweet_media_ids"]:
                        new_relation = MediasTweets(
                            tweet_id=new_tweet.id,
                            media_id=m_id,
                        )
                        session.add(new_relation)
                await session.commit()
                result, code = {"result": True, "tweet_id": new_tweet.id}, 201
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            if "violates foreign key constraint" in str(err):
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "Media does not exist.",
                }, 404
            else:
                result, code = {
                    "result": False,
                    "error_type": "SQLAlchemyError",
                    "error_message": str(err),
                }, 500

        return ResponseData(response=result, status_code=code)

    @classmethod
    async def delete(
        cls,
        user_id: int,
        tweet_id: int,
        async_session: AsyncSession,
    ) -> ResponseData:
        """Delete tweet from tweets table.

        Parameters:
            user_id: int
            tweet_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
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
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)


class LikesMethods(Likes):
    """Class with Orm methods for Likes table."""

    @classmethod
    async def add(
        cls,
        user_id: int,
        tweet_id: int,
        async_session: AsyncSession,
    ) -> ResponseData:
        """Add like to likes table.

        Parameters:
            user_id: int
            tweet_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                new_like = Likes(user_id=user_id, tweet_id=tweet_id)
                session.add(new_like)
                await session.commit()
            result, code = {"result": True}, 201
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            if "duplicate key value violates unique constraint" in str(err):
                result, code = {
                    "result": False,
                    "error_type": "UniqueViolationError",
                    "error_message": "Like already exists.",
                }, 400
            elif "violates foreign key constraint" in str(err):
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "User does not exist.",
                }, 404
            else:
                result, code = {
                    "result": False,
                    "error_type": "InternalServerError",
                    "error_message": str(err),
                }, 500

        return ResponseData(response=result, status_code=code)

    @classmethod
    async def delete(
        cls,
        user_id: int,
        tweet_id: int,
        async_session: AsyncSession,
    ) -> ResponseData:
        """Delete like from likes table.

        Parameters:
            user_id: int
            tweet_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                check_like_exists_exp = select(Likes).where(
                    and_(Likes.user_id == user_id, Likes.tweet_id == tweet_id),
                )
                check_request = await session.execute(check_like_exists_exp)
                check_result = check_request.scalars().one_or_none()

                if check_result:
                    expression = delete(Likes).where(
                        and_(Likes.user_id == user_id, Likes.tweet_id == tweet_id),
                    )
                    await session.execute(expression)
                    await session.commit()
                    result, code = {"result": True}, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "DataNotFound",
                        "error_message": "Like doesn't exist.",
                    }, 404
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500
        return ResponseData(response=result, status_code=code)
