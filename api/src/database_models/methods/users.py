from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func

from database_models.users_orm_models import Users, Followers, Cookies


class CookiesMethods(Cookies):
    @classmethod
    async def add(cls, user_id: int, api_key: str, async_session: AsyncSession) -> dict:
        async with async_session as session:
            new_key = Cookies(user_id=user_id, hash=func.crypt(api_key, func.gen_salt("md5")))
            session.add(new_key)
            await session.commit()
            return {"result": True}

    @classmethod
    async def get_user_id(cls, api_key: str, async_session) -> dict:
        async with async_session as session:
            expression = select(Cookies).where(Cookies.hash == func.crypt(api_key, Cookies.hash))
            request = await session.execute(expression)

            matched_key = request.scalars().one_or_none()
            if matched_key:
                user_id = matched_key.user_id
                return {"result": True, "user_id": user_id}
            else:
                return {"result": False,
                        "error_type": "DataNotFound",
                        "error_message": "User with provided api-key not found"
                        }