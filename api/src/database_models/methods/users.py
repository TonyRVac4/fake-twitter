from sqlalchemy import and_, delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from database_models.db_config import ResponseData  # noqa
from database_models.users_orm_models import Cookies, Followers, Users  # noqa
from utils.logger_config import orm_logger  # noqa


class UsersMethods(Users):
    """Class with Orm methods for Users table."""

    @classmethod
    async def get_info_by_id(
        cls, user_id: int, async_session: AsyncSession,
    ) -> ResponseData:
        """Return user profile info by id.

        Parameters:
            user_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                expression = (
                    select(Users).
                    where(Users.id == user_id).
                    options(
                        selectinload(Users.followers).selectinload(
                            Followers.follower,
                        ),  # Загрузка follower в followers
                        selectinload(Users.following).selectinload(
                            Followers.user,
                        ),  # Загрузка user в following
                    )
                )
                request = await session.execute(expression)
                user_data = request.scalars().one_or_none()

                if user_data:
                    followers: list = [
                        {
                            "id": follower.follower_id,
                            "name": follower.follower.username,
                        }
                        for follower in user_data.followers
                    ]
                    following: list = [
                        {
                            "id": following.user_id,
                            "name": following.user.username,
                        }
                        for following in user_data.following
                    ]

                    result, code = {
                        "result": True,
                        "user": {
                            "id": user_data.id,
                            "name": user_data.username,
                            "followers": followers,
                            "following": following,
                        },
                    }, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "DataNotFound",
                        "error_message": "User does not exist.",
                    }, 404
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)


class FollowersMethods(Followers):
    """Class with Orm methods for Followers table."""

    @classmethod
    async def add(
        cls, follower_id: int, following_id: int, async_session: AsyncSession,
    ) -> ResponseData:
        """Add follow to followers table.

        Parameters:
            follower_id: int
            following_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        if following_id == follower_id:
            return ResponseData(
                response={
                    "result": False,
                    "error_type": "ValueError",
                    "error_message": "You can't follow yourself!",
                },
                status_code=400,
            )

        try:
            async with async_session as session:
                new_follower = Followers(user_id=following_id, follower_id=follower_id)
                session.add(new_follower)
                await session.commit()
                result, code = {"result": True}, 201
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            if "duplicate key value violates unique constraint" in str(err):
                result, code = {
                    "result": False,
                    "error_type": "UniqueViolationError",
                    "error_message": "Follow already exists.",
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
        cls, follower_id: int, following_id: int, async_session: AsyncSession,
    ) -> ResponseData:
        """Delete follow from followers table.

        Parameters:
            follower_id: int
            following_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                check_follow_exists_exp = select(Followers).where(
                    and_(
                        Followers.user_id == following_id,
                        Followers.follower_id == follower_id,
                    ),
                )
                check_request = await session.execute(check_follow_exists_exp)
                check_result = check_request.scalars().one_or_none()

                if check_result:
                    del_expr = delete(Followers).where(
                        and_(
                            Followers.user_id == following_id,
                            Followers.follower_id == follower_id,
                        ),
                    )
                    await session.execute(del_expr)
                    await session.commit()
                    result, code = {"result": True}, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "DataNotFound",
                        "error_message": "Follow does not exist.",
                    }, 404
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)


class CookiesMethods(Cookies):
    """Class with Orm methods for Cookies table."""

    @classmethod
    async def add(
        cls, user_id: int, api_key: str, async_session: AsyncSession,
    ) -> ResponseData:
        """Add api key to Cookies table.

        Parameters:
            user_id: int
            api_key: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                check_expr = select(Cookies).where(
                    Cookies.hash == func.crypt(api_key, Cookies.hash),
                )
                request = await session.execute(check_expr)
                result = request.scalars().one_or_none()

                if result is None:
                    new_key = Cookies(
                        user_id=user_id, hash=func.crypt(api_key, func.gen_salt("md5")),
                    )
                    session.add(new_key)
                    await session.commit()
                    result, code = {"result": True}, 201
                else:
                    result, code = {
                        "result": False,
                        "error_type": "UniqueViolationError",
                        "error_message": "Key already exists.",
                    }, 400
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)

    @classmethod
    async def get_user_id(
        cls, api_key: str, async_session: AsyncSession,
    ) -> ResponseData:
        """Return api key by user id from Cookies table.

        Parameters:
            api_key: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                expression = select(Cookies).where(
                    Cookies.hash == func.crypt(api_key, Cookies.hash),
                )
                request = await session.execute(expression)

                matched_key = request.scalars().one_or_none()
                if matched_key:
                    user_id = matched_key.user_id
                    result, code = {"result": True, "user_id": user_id}, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "Unauthorized",
                        "error_message": "User with provided api-key not found",
                    }, 401
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)
