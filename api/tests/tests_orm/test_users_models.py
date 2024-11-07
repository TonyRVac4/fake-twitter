from sqlalchemy.ext.asyncio import AsyncSession
from src.database_models.methods.users import UsersMethods, FollowersMethods, CookiesMethods  # noqa


async def test_1(async_session: AsyncSession):
    assert 1 == 1
