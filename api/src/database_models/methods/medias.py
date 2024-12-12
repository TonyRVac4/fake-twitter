from sqlalchemy import delete, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database_models.db_config import ResponseData  # noqa
from database_models.tweets_orm_models import MediasTweets, Medias  # noqa
from utils.logger_config import orm_logger  # noqa


class MediasMethods(Medias):
    """Class with Orm methods for Medias table."""

    @classmethod
    async def get_by_tweet_id(
        cls, tweet_id: int, async_session: AsyncSession,
    ) -> ResponseData:
        """Return links by tweet id.

        Parameters:
            tweet_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                expr = (
                    select(Medias.link).
                    join(MediasTweets, MediasTweets.media_id == Medias.id).
                    where(MediasTweets.tweet_id == tweet_id)
                )
                request = await session.execute(expr)
                data: list = request.scalars().fetchall()
                if data:
                    result, code = {"result": True, "links": data}, 200
                else:
                    result, code = {"result": False}, 404
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500
        return ResponseData(response=result, status_code=code)

    @classmethod
    async def add(
        cls, link: str, async_session: AsyncSession,
    ) -> ResponseData:
        """Add tweet id and link to the medias table.

        Parameters:
            link: str
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                new_media = Medias(link=link)
                session.add(new_media)
                await session.commit()
                result, code = {"result": True, "media_id": new_media.id}, 201
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500

        return ResponseData(response=result, status_code=code)

    @classmethod
    async def delete(cls, media_id: int, async_session: AsyncSession) -> ResponseData:
        """Delete media by id.

        Parameters:
            media_id: int
            async_session: AsyncSession

        Returns:
            ResponseData
        """
        try:
            async with async_session as session:
                check_media_exists_exp = select(Medias).where(Medias.id == media_id)
                check_request = await session.execute(check_media_exists_exp)
                check_result = check_request.scalars().one_or_none()

                if check_result:
                    del_expr = delete(Medias).where(Medias.id == media_id)
                    await session.execute(del_expr)
                    await session.commit()
                    result, code = {"result": True}, 200
                else:
                    result, code = {
                        "result": False,
                        "error_type": "DataNotFound",
                        "error_message": "Media does not exist.",
                    }, 404
        except SQLAlchemyError as err:
            orm_logger.exception(str(err))
            result, code = {
                "result": False,
                "error_type": "SQLAlchemyError",
                "error_message": str(err),
            }, 500
        return ResponseData(response=result, status_code=code)
