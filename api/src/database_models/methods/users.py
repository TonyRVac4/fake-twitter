from sqlalchemy import select, delete, and_
from sqlalchemy.sql import func
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from database_models.users_orm_models import Users, Followers, Cookies  # noqa
from database_models.db_config import ResponseData  # noqa


class UsersMethods(Users):
    @classmethod
    async def get_info_by_id(cls, user_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            expression = select(Users).where(Users.id == user_id).options(
                    selectinload(Users.followers).selectinload(Followers.follower),  # Загрузка follower в followers
                    selectinload(Users.following).selectinload(Followers.user)       # Загрузка user в following
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
        return ResponseData(response=result, status_code=code)


class FollowersMethods(Followers):
    @classmethod
    async def add(cls, follower_id: int, following_id: int, async_session: AsyncSession) -> ResponseData:
        if following_id == follower_id:
            return ResponseData(
                response={
                    "result": False,
                    "error_type": "ValueError",
                    "error_message": "You can't follow yourself!",
                }, status_code=400
            )

        try:
            async with async_session as session:
                new_follower = Followers(user_id=following_id, follower_id=follower_id)
                session.add(new_follower)
                await session.commit()
                result, code = {"result": True}, 201
        except IntegrityError as exp:
            if 'duplicate key value violates unique constraint' in str(exp):
                result, code = {
                    "result": False,
                    "error_type": "UniqueViolationError",
                    "error_message": "Follow already exists.",
                }, 400
            elif 'violates foreign key constraint' in str(exp):
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "User does not exist.",
                }, 404
            else:
                result, code = {
                    "result": False,
                    "error_type": "InternalServerError",
                    "error_message": exp.orig,
                }, 500
        return ResponseData(response=result, status_code=code)

    @classmethod
    async def delete(cls, follower_id: int, following_id: int, async_session: AsyncSession) -> ResponseData:
        async with async_session as session:
            check_follow_exists_exp = select(Followers).where(and_(
                        Followers.user_id == following_id,
                        Followers.follower_id == follower_id
                    ))
            check_request = await session.execute(check_follow_exists_exp)
            check_result = check_request.scalars().one_or_none()

            if check_result:
                del_expr = delete(Followers).where(and_(
                    Followers.user_id == following_id,
                    Followers.follower_id == follower_id
                ))
                await session.execute(del_expr)
                await session.commit()
                result, code = {"result": True}, 200
            else:
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "Follow does not exist.",
                }, 404

        return ResponseData(response=result, status_code=code)


class CookiesMethods(Cookies):
    @classmethod
    async def add(cls, user_id: int, api_key: str, async_session: AsyncSession) -> dict:
        async with async_session as session:
            new_key = Cookies(user_id=user_id, hash=func.crypt(api_key, func.gen_salt("md5")))
            session.add(new_key)
            await session.commit()
            return ResponseData(response={"result": True}, status_code=201)

    @classmethod
    async def get_user_id(cls, api_key: str, async_session: AsyncSession) -> dict:
        async with async_session as session:
            expression = select(Cookies).where(Cookies.hash == func.crypt(api_key, Cookies.hash))
            request = await session.execute(expression)

            matched_key = request.scalars().one_or_none()
            if matched_key:
                user_id = matched_key.user_id
                result, code = {"result": True, "user_id": user_id}, 200
            else:
                result, code = {
                    "result": False,
                    "error_type": "DataNotFound",
                    "error_message": "User with provided api-key not found"
                }, 404
            return ResponseData(response=result, status_code=code)
