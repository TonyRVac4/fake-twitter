from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from database_models.users_orm_models import Users, Followers, Cookies
from database_models.tweets_orm_models import Tweets, Medias, Likes
from database_models.db_config import base_metadata, engine
from database_models.methods.users import CookiesMethods


async def setup_test_data(async_session: AsyncSession):
    async with engine.connect() as conn:
        await conn.run_sync(base_metadata.drop_all)
        await conn.run_sync(base_metadata.create_all)
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS pgcrypto;"))
        # необходим для коректной раброты генерации хэша
        await conn.commit()

    async with async_session as session:
        user1 = Users(username="Tony", email="spacexsn23@gmail.com")
        user2 = Users(username="Kris", email="catsdogs23@gmail.com")

        user_follower1 = Users(username="jack follower", email="grqefwdsa@gmail.com")
        user_follower2 = Users(username="mark follower", email="ewfaEgr4@gmail.com")
        session.add_all([user1, user2, user_follower1, user_follower2])
        await session.commit()

        follow1 = Followers(user_id=user1.id, follower_id=user_follower1.id)
        follow2 = Followers(user_id=user1.id, follower_id=user_follower2.id)
        follow3 = Followers(user_id=user1.id, follower_id=user2.id)

        follow4 = Followers(user_id=user2.id, follower_id=user_follower1.id)
        follow5 = Followers(user_id=user2.id, follower_id=user_follower2.id)
        session.add_all([follow1, follow2, follow3, follow4, follow5])
        await session.commit()

        tweet1 = Tweets(user_id=user1.id, data="SpaceX has successfully launched their 1st heavy rocket")
        tweet2 = Tweets(user_id=user1.id, data="Booster SN23 has landed on the tower's chopsticks")
        tweet3 = Tweets(user_id=user2.id, data="Cutie cats")
        tweet4 = Tweets(user_id=user2.id, data="Cutie dogs")
        session.add_all([tweet1, tweet2,tweet3,tweet4])
        await session.commit()

        media1 = Medias(tweet_id=tweet1.id, data="link1")
        media2 = Medias(tweet_id=tweet3.id, data="link2")
        media3 = Medias(tweet_id=tweet3.id, data="link3")
        session.add_all([media1, media2, media3])
        await session.commit()

        like1 = Likes(user_id=user1.id, tweet_id=tweet3.id)
        like2 = Likes(user_id=user1.id, tweet_id=tweet4.id)
        like3 = Likes(user_id=user2.id, tweet_id=tweet1.id)
        like4 = Likes(user_id=user2.id, tweet_id=tweet2.id)
        like5 = Likes(user_id=user2.id, tweet_id=tweet3.id)
        like6 = Likes(user_id=user2.id, tweet_id=tweet4.id)
        session.add_all([like1, like2, like3, like4, like5, like6])
        await session.commit()
    """
    1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p
    q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6
    z9x8c7v6b5n4m3l2k1j0h9g8f7d6s5a4
    """
    await CookiesMethods.add(user_id=1,
                             api_key="1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p",
                             async_session=async_session
                             )
    await CookiesMethods.add(user_id=1,
                             api_key="q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6",
                             async_session=async_session
                             )
    await CookiesMethods.add(user_id=2,
                             api_key="z9x8c7v6b5n4m3l2k1j0h9g8f7d6s5a4",
                             async_session=async_session
                             )
