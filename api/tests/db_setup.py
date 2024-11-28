from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from database_models.tweets_orm_models import Likes, MediasTweets, Medias, Tweets # noqa
from database_models.users_orm_models import Cookies, Followers, Users  # noqa


async def setup_test_data(async_session: AsyncSession):
    """Fill up the test db with data.

    Parameters:
        async_session: AsyncSession
    """
    async with async_session as session:
        user1 = Users(username="Tony", email="spacexsn23@gmail.com")
        user2 = Users(username="Kris", email="catsdogs23@gmail.com")
        user3 = Users(username="David", email="hihiun23@gmail.com")
        user_follower1 = Users(username="jack follower", email="grqefwdsa@gmail.com")
        user_follower2 = Users(username="mark follower", email="ewfaEgr4@gmail.com")
        session.add_all([user1, user2, user3, user_follower1, user_follower2])

        follow1 = Followers(user_id=user1.id, follower_id=user_follower1.id)
        follow2 = Followers(user_id=user2.id, follower_id=user_follower2.id)
        session.add_all([follow1, follow2])

        tweet1 = Tweets(
            user_id=user1.id,
            data="SpaceX has successfully launched their 1st heavy rocket",
        )
        tweet2 = Tweets(
            user_id=user1.id,
            data="Booster SN23 has landed on the tower's chopsticks",
        )
        tweet3 = Tweets(user_id=user2.id, data="Cutie cats")
        tweet4 = Tweets(user_id=user3.id, data="Random data1")
        tweet5 = Tweets(user_id=user3.id, data="Random data2")
        image1 = Medias(
            link="https://s3.timeweb.cloud/37634968-test-backet/cat1.jpg",
        )
        image2 = Medias(
            link="https://s3.timeweb.cloud/37634968-test-backet/cat2.jpg",
        )
        image3 = Medias(
            link="https://s3.timeweb.cloud/37634968-test-backet/cat1.jpg",
        )
        image4 = Medias(
            link="https://s3.timeweb.cloud/37634968-test-backet/cat2.jpg",
        )
        session.add_all([tweet1, tweet2, tweet3, tweet4, tweet5])
        session.add_all([image1, image2, image3, image4])

        relation1 = MediasTweets(tweet_id=tweet4.id, media_id=image1.id)
        relation2 = MediasTweets(tweet_id=tweet4.id, media_id=image2.id)
        session.add_all([relation1, relation2])

        key1 = Cookies(
            user_id=user1.id,
            hash=func.crypt("1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p", func.gen_salt("md5")),
        )
        key2 = Cookies(
            user_id=user2.id,
            hash=func.crypt("q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6", func.gen_salt("md5")),
        )
        key3 = Cookies(
            user_id=user3.id,
            hash=func.crypt("z9x8c7v6b5n4m3l2k1j0h9g8f7d6s5a4", func.gen_salt("md5")),
        )
        session.add_all([key1, key2, key3])
        await session.commit()
