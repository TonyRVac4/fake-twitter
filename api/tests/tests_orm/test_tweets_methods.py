from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database_models.methods.tweets import LikesMethods, TweetsMethods  # noqa
from src.schemas import Pagination  # noqa
from database_models.tweets_orm_models import Likes, MediasTweets, Medias, Tweets  # noqa


async def test_get_posts_for_user(async_session: AsyncSession):
    """Test TweetsMethods.get_posts_for_user() method.

    Return list of posts for user by id.

    Parameters:
        async_session: AsyncSession
    """
    request = await TweetsMethods.get_posts_list(
        user_id=1,
        pagination=Pagination(offset=None, limit=None),
        async_session=async_session,
    )

    assert request.status_code == 200
    assert request.response.get("result") is True


async def test_add_tweet_with_no_media(async_session: AsyncSession):
    """Test TweetsMethods.add() method with no media.

    Add new tweet to the table with no media.

    Parameters:
        async_session: AsyncSession
    """
    test_data = {"tweet_data": "test data 1", "tweet_media_ids": []}

    request = await TweetsMethods.add(
        user_id=1,
        data=test_data,
        async_session=async_session,
    )
    tweet_id = request.response.get("tweet_id")

    assert request.status_code == 201
    assert tweet_id is not None

    async with async_session as session:
        check_expr = select(Tweets).where(Tweets.id == tweet_id)
        check_request = await session.execute(check_expr)
        result = check_request.scalars().one_or_none()

        assert result is not None
        assert result.id == tweet_id
        assert result.data == test_data["tweet_data"]


async def test_add_tweet_with_media(async_session: AsyncSession):
    """Test TweetsMethods.add() method with media.

    Add new tweet to the table with media.

    Parameters:
        async_session: AsyncSession
    """
    test_data = {"tweet_data": "test data 2", "tweet_media_ids": [3, 4]}

    request = await TweetsMethods.add(
        user_id=1,
        data=test_data,
        async_session=async_session,
    )
    tweet_id = request.response.get("tweet_id")

    assert request.status_code == 201
    assert tweet_id is not None

    async with async_session as session:
        check_tweet_expr = select(Tweets).where(Tweets.id == tweet_id)
        check_tweet_request = await session.execute(check_tweet_expr)
        check_tweet_result = check_tweet_request.scalars().one_or_none()

        assert check_tweet_result.id == tweet_id
        assert check_tweet_result.data == test_data["tweet_data"]

        check_media_relation_expr = select(MediasTweets).where(
            and_(
                MediasTweets.tweet_id == tweet_id,
                MediasTweets.media_id == test_data["tweet_media_ids"][0],
            ),
        )
        check_media_relation_request = await session.execute(check_media_relation_expr)
        check_relation_result = check_media_relation_request.scalars().one_or_none()

        assert check_relation_result is not None


async def test_cant_add_tweet_with_nonexistent_medias(async_session: AsyncSession):
    """Test TweetsMethods.add() method.

    Can't add tweet if medias doesn't exist.

    Parameters:
        async_session: AsyncSession
    """
    data = {"tweet_data": "Hello, world!", "tweet_media_ids": [7, 8]}

    request = await TweetsMethods.add(
        user_id=1,
        data=data,
        async_session=async_session,
    )
    assert request.status_code == 404
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "DataNotFound"


async def test_delete_tweet(async_session: AsyncSession):
    """Test TweetsMethods.delete() method.

     Delete tweet from the table.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 2
    check_expr = select(Tweets).where(Tweets.id == tweet_id)

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        result_before = check_request_before.scalars().one_or_none()
        assert result_before is not None
        assert result_before.id == tweet_id

        request = await TweetsMethods.delete(
            user_id=1,
            tweet_id=tweet_id,
            async_session=async_session,
        )
        assert request.status_code == 200
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        result_after = check_request_after.scalars().one_or_none()
        assert result_after is None


async def test_can_not_delete_other_person_tweet(async_session: AsyncSession):
    """Test TweetsMethods.delete() method.

     Can not delete other person tweet from the table.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 3
    request = await TweetsMethods.delete(
        user_id=1,
        tweet_id=tweet_id,
        async_session=async_session,
    )
    assert request.status_code == 401
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "ActionForbidden"


async def test_can_not_delete_nonexistent_tweet(async_session: AsyncSession):
    """Test TweetsMethods.delete() method.

     Can not delete tweet from the table if it does not exist.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 12
    request = await TweetsMethods.delete(
        user_id=1,
        tweet_id=tweet_id,
        async_session=async_session,
    )
    assert request.status_code == 404
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "DataNotFound"


async def test_add_new_like(async_session: AsyncSession):
    """Test LikesMethods.add() method.

    Add like to the table.

    Parameters:
        async_session: AsyncSession
    """
    user_id = 1
    tweet_id = 3
    check_expr = select(Likes).where(and_(
        Likes.user_id == user_id, Likes.tweet_id == tweet_id,
    ))

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        result_before = check_request_before.scalars().one_or_none()
        assert result_before is None

        request = await LikesMethods.add(
            user_id=user_id,
            tweet_id=tweet_id,
            async_session=async_session,
        )
        assert request.status_code == 201
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        result_after = check_request_after.scalars().one_or_none()
        assert result_after.user_id == user_id
        assert result_after.tweet_id == tweet_id


async def test_can_not_add_existent_like(async_session: AsyncSession):
    """Test LikesMethods.add() method.

    Can not add like to the table if it already exists.

    Parameters:
        async_session: AsyncSession
    """
    user_id = 1
    tweet_id = 3

    async with async_session as session:
        check_expr = select(Likes).where(and_(
            Likes.user_id == user_id, Likes.tweet_id == tweet_id,
        ))
        check_request_after = await session.execute(check_expr)
        result_after = check_request_after.scalars().one_or_none()
        assert result_after is not None
        assert result_after.user_id == user_id
        assert result_after.tweet_id == tweet_id

    request = await LikesMethods.add(
        user_id=user_id,
        tweet_id=tweet_id,
        async_session=async_session,
    )
    assert request.status_code == 400
    assert request.response.get("result") is False


async def test_delete_like(async_session: AsyncSession):
    """Test LikesMethods.delete() method.

    Delete like from the table.

    Parameters:
        async_session: AsyncSession
    """
    user_id = 1
    tweet_id = 3
    check_expr = select(Likes).where(and_(
        Likes.user_id == user_id, Likes.tweet_id == tweet_id,
    ))

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        result_before = check_request_before.scalars().one_or_none()
        assert result_before.tweet_id == tweet_id
        assert result_before.user_id == user_id

        request = await LikesMethods.delete(
            user_id=user_id,
            tweet_id=tweet_id,
            async_session=async_session,
        )
        assert request.status_code == 200
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        result_after = check_request_after.scalars().one_or_none()
        assert result_after is None


async def test_can_not_delete_nonexistent_like(async_session: AsyncSession):
    """Test LikesMethods.delete() method.

    Can not delete like from the table if it does not exist.

    Parameters:
        async_session: AsyncSession
    """
    request = await LikesMethods.delete(
        user_id=1,
        tweet_id=15,
        async_session=async_session,
    )
    assert request.status_code == 404
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "DataNotFound"
