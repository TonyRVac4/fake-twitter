from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database_models.methods.users import UsersMethods, FollowersMethods, CookiesMethods  # noqa
from database_models.users_orm_models import Users, Followers, Cookies # noqa


async def test_get_user_info_by_id(async_session: AsyncSession):
    """Test users method: return info about user by id.

    Parameters:
        async_session: AsyncSession
    """
    request = await UsersMethods.get_info_by_id(
        user_id=2,
        async_session=async_session,
    )

    assert request.status_code == 200
    assert request.response.get("result") is True


async def test_can_not_get_nonexistence_users_info_by_id(async_session: AsyncSession):
    """Test users method: can not return info about user who does not exist.

    Parameters:
        async_session: AsyncSession
    """
    request = await UsersMethods.get_info_by_id(
        user_id=22,
        async_session=async_session,
    )

    assert request.status_code == 404
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "DataNotFound"


async def test_follow_user(async_session: AsyncSession):
    """Test follow method: add follow to the table.

    Parameters:
        async_session: AsyncSession
    """
    follower_id = 2
    following_id = 1

    check_expr = select(Followers).where(and_(
        Followers.user_id == following_id,
        Followers.follower_id == follower_id)
    )

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()
        assert check_result_before is None

        request = await FollowersMethods.add(
            follower_id=follower_id,
            following_id=following_id,
            async_session=async_session,
        )
        assert request.status_code == 201
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().one_or_none()
        assert check_result_after is not None
        assert check_result_after.user_id == following_id
        assert check_result_after.follower_id == follower_id


async def test_can_not_follow_yourself(async_session: AsyncSession):
    """Test follows method: can not add follow to the table where user follows themselves.

    Parameters:
        async_session: AsyncSession
    """
    request = await FollowersMethods.add(
        follower_id=2,
        following_id=2,
        async_session=async_session,
    )

    assert request.status_code == 400
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "ValueError"


async def test_can_not_follow_already_followed_user(async_session: AsyncSession):
    """Test follows method: can not add follow to the table if it already exists.

    Parameters:
        async_session: AsyncSession
    """
    request = await FollowersMethods.add(
        follower_id=2,
        following_id=1,
        async_session=async_session,
    )

    assert request.status_code == 400
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "UniqueViolationError"


async def test_can_not_follow_nonexistence_user(async_session: AsyncSession):
    """Test follows method: can not add follow to the table if the user does not exist.

    Parameters:
        async_session: AsyncSession
    """
    request = await FollowersMethods.add(
        follower_id=2,
        following_id=11,
        async_session=async_session,
    )

    assert request.status_code == 404
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "DataNotFound"


async def test_unfollow_user(async_session: AsyncSession):
    """Test follows method: delete follow from the table.

    Parameters:
        async_session: AsyncSession
    """
    follower_id = 2
    following_id = 1

    check_expr = select(Followers).where(and_(
        Followers.user_id == following_id,
        Followers.follower_id == follower_id)
    )

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()

        assert check_result_before is not None
        assert check_result_before.user_id == following_id
        assert check_result_before.follower_id == follower_id

        request = await FollowersMethods.delete(
            follower_id=follower_id,
            following_id=following_id,
            async_session=async_session,
        )
        assert request.status_code == 200
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().one_or_none()
        assert check_result_after is None


async def test_can_not_unfollow_not_followed_user(async_session: AsyncSession):
    """Test follows method: can not delete follow from the table if it does not exist.

    Parameters:
        async_session: AsyncSession
    """
    request = await FollowersMethods.delete(
        follower_id=2,
        following_id=1,
        async_session=async_session,
    )

    assert request.status_code == 404
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "DataNotFound"


async def test_add_new_api_key(async_session: AsyncSession):
    """Test cookies method: add new encrypted api-key to the table.

    Parameters:
        async_session: AsyncSession
    """
    key = "lk0zc7v6b5n4l1l2k1j0m9g8f7d6s5a0"
    user_id = 2
    check_expr = select(Cookies).where(Cookies.hash == func.crypt(key, Cookies.hash))

    async with async_session as session:
        check_request_before = await session.execute(check_expr)
        check_result_before = check_request_before.scalars().one_or_none()
        assert check_result_before is None

        request = await CookiesMethods.add(
            user_id=user_id,
            api_key=key,
            async_session=async_session,
        )
        assert request.status_code == 201
        assert request.response.get("result") is True

        check_request_after = await session.execute(check_expr)
        check_result_after = check_request_after.scalars().one_or_none()
        assert check_result_after is not None
        assert check_result_after.user_id == user_id


async def test_can_not_add_existing_api_key(async_session: AsyncSession):
    """Test cookies method: can not add new encrypted api-key to the table if it already exists.

    Parameters:
        async_session: AsyncSession
    """
    request = await CookiesMethods.add(
        user_id=2,
        api_key="lk0zc7v6b5n4l1l2k1j0m9g8f7d6s5a0",
        async_session=async_session,
    )

    assert request.status_code == 400
    assert request.response.get("result") is False
    assert request.response.get("error_type") == "UniqueViolationError"
