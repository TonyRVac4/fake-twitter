from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.database_models.methods.tweets import LikesMethods, TweetsMethods  # noqa
from src.database_models.methods.medias import MediasMethods  # noqa
from database_models.tweets_orm_models import Likes, Medias, Tweets  # noqa


async def test_get_by_tweet_id(async_session: AsyncSession):
    """Test MediasMethods.get_by_tweet_id() method.

    Return list of medias by tweet id.

    Parameters:
        async_session: AsyncSession
    """
    request = await MediasMethods.get_by_tweet_id(
        tweet_id=1,
        async_session=async_session,
    )
    assert request.status_code == 200
    assert request.response.get("result") is True
    assert len(request.response.get("links")) > 0


async def test_get_by_tweet_id_with_no_media(async_session: AsyncSession):
    """Test MediasMethods.get_by_tweet_id() method.

    Can't return list of medias by tweet id if it has no media.

    Parameters:
        async_session: AsyncSession
    """

    request = await MediasMethods.get_by_tweet_id(
        tweet_id=3,
        async_session=async_session,
    )
    assert request.status_code == 404
    assert request.response.get("result") is False


async def test_get_by_nonexistent_tweet_id(async_session: AsyncSession):
    """Test MediasMethods.get_by_tweet_id() method.

    Can't return list of medias by tweet id if tweet doesn't exist.

    Parameters:
        async_session: AsyncSession
    """
    request = await MediasMethods.get_by_tweet_id(
        tweet_id=12,
        async_session=async_session,
    )
    assert request.status_code == 404
    assert request.response.get("result") is False


async def test_add_media_link(async_session: AsyncSession):
    """Test MediasMethods.add() method.

    Add media link to medias table.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 2
    link = "https://s3.timeweb.cloud/37634968-test-backet/meme1.jpg"

    check_expr = select(Medias).where(and_(
        Medias.tweet_id == tweet_id,
        Medias.link == link,
    ))

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()
        assert check_result_before is None

        request = await MediasMethods.add(
            tweet_id=tweet_id,
            link=link,
            async_session=async_session,
        )
        assert request.status_code == 201
        assert request.response.get("result") is True
        assert request.response.get("media_id") is not None

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().one_or_none()
        assert check_result_after.tweet_id == tweet_id
        assert check_result_after.link == link


async def test_can_not_add_media_link_if_tweet_does_not_exist(async_session: AsyncSession):
    """Test MediasMethods.add() method.

    Can't add media link to medias table if tweet doesn't exist.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 22
    link = "https://s3.timeweb.cloud/37634968-test-backet/meme1.jpg"

    check_expr = select(Medias).where(and_(
        Medias.tweet_id == tweet_id,
        Medias.link == link,
    ))

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()
        assert check_result_before is None

        request = await MediasMethods.add(
            tweet_id=tweet_id,
            link=link,
            async_session=async_session,
        )
        assert request.status_code == 404
        assert request.response.get("result") is False
        assert request.response.get("error_type") == "DataNotFound"

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().one_or_none()
        assert check_result_after is None


async def test_delete_by_media_id(async_session: AsyncSession):
    """Test MediasMethods.delete() method.

    Delete media link by id.

    Parameters:
        async_session: AsyncSession
    """
    media_id = 2

    check_expr = select(Medias).where(Medias.id == media_id)

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()
        assert check_result_before is not None
        assert check_result_before.id == media_id

        request = await MediasMethods.delete(
            media_id=media_id,
            async_session=async_session,
        )
        assert request.status_code == 200
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().one_or_none()
        assert check_result_after is None


async def test_delete_by_nonexistent_media_id(async_session: AsyncSession):
    """Test MediasMethods.delete() method.

    Can't delete media link by id if it doesn't exist.

    Parameters:
        async_session: AsyncSession
    """
    media_id = 22

    check_expr = select(Medias).where(Medias.id == media_id)

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()
        assert check_result_before is None

        request = await MediasMethods.delete(
            media_id=22,
            async_session=async_session,
        )
        assert request.status_code == 404
        assert request.response.get("result") is False
        assert request.response.get("error_type") == "DataNotFound"


async def test_delete_all_media_by_tweet_id(async_session: AsyncSession):
    """Test MediasMethods.delete_all_by_tweet_id() method.

    Delete media links by tweet id.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 1

    check_expr = select(Medias).where(Medias.tweet_id == tweet_id)

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().fetchall()
        assert len(check_result_before) > 0
        assert check_result_before[0].tweet_id == tweet_id

        request = await MediasMethods.delete_all_by_tweet_id(
            tweet_id=tweet_id,
            async_session=async_session,
        )
        assert request.status_code == 200
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().fetchall()
        assert len(check_result_after) == 0


async def test_can_not_delete_media_by_nonexistent_tweet_id(async_session: AsyncSession):
    """Test MediasMethods.delete_all_by_tweet_id() method.

    Can't delete media links by tweet id if tweet doesn't exist.

    Parameters:
        async_session: AsyncSession
    """
    tweet_id = 12

    check_expr = select(Medias).where(Medias.tweet_id == tweet_id)

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().fetchall()
        assert len(check_result_before) == 0

        request = await MediasMethods.delete_all_by_tweet_id(
            tweet_id=12,
            async_session=async_session,
        )
        assert request.status_code == 404
        assert request.response.get("result") is False
        assert request.response.get("error_type") == "DataNotFound"
