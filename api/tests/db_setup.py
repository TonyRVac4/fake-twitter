from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from database_models.tweets_orm_models import Likes, Medias, Tweets  # noqa
from database_models.users_orm_models import Cookies, Followers, Users  # noqa


async def setup_test_data(async_session: AsyncSession):
    """Fill up the test db with data.

    Parameters:
        async_session: AsyncSession
    """
    async with async_session as session:
        user1 = Users(username="Tony", email="spacexsn23@gmail.com")
        user2 = Users(username="Kris", email="catsdogs23@gmail.com")
        user_follower1 = Users(username="jack follower", email="grqefwdsa@gmail.com")
        user_follower2 = Users(username="mark follower", email="ewfaEgr4@gmail.com")
        session.add_all([user1, user2, user_follower1, user_follower2])
        await session.commit()

        follow1 = Followers(user_id=user1.id, follower_id=user_follower1.id)
        follow2 = Followers(user_id=user2.id, follower_id=user_follower2.id)
        tweet1 = Tweets(
            user_id=user1.id,
            data="SpaceX has successfully launched their 1st heavy rocket",
        )
        tweet2 = Tweets(
            user_id=user1.id,
            data="Booster SN23 has landed on the tower's chopsticks",
        )
        tweet3 = Tweets(user_id=user2.id, data="Cutie cats")
        session.add_all([follow1, follow2, tweet1, tweet2, tweet3])
        await session.commit()

        media1 = Medias(tweet_id=tweet1.id, data="link1")
        media2 = Medias(tweet_id=tweet2.id, data="link2")
        media3 = Medias(tweet_id=tweet2.id, data="link3")
        session.add_all([media1, media2, media3])
        await session.commit()

        key1 = Cookies(
            user_id=user1.id,
            hash=func.crypt("1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p", func.gen_salt("md5")),
        )
        key2 = Cookies(
            user_id=user1.id,
            hash=func.crypt("q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6", func.gen_salt("md5")),
        )
        key3 = Cookies(
            user_id=user2.id,
            hash=func.crypt("z9x8c7v6b5n4m3l2k1j0h9g8f7d6s5a4", func.gen_salt("md5")),
        )
        session.add_all([key1, key2, key3])
        await session.commit()
