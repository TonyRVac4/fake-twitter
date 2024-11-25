from typing import Annotated

from fastapi import APIRouter, Depends, Form, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_s3 import Client
from schemas import MediaUploadResponseDataWithId  # noqa
from database_models.db_config import ResponseData, get_async_session  # noqa
from database_models.methods.medias import MediasMethods  # noqa
from database_models.methods.tweets import TweetsMethods  # noqa
from utils.s3_config import get_async_s3_client  # noqa

router = APIRouter(
    prefix="/api/medias",
)


@router.post("", response_model=MediaUploadResponseDataWithId)
async def upload_media_from_post(
    tweet_id: Annotated[int, Form()],
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session),
    s3_client: Client = Depends(get_async_s3_client),
):
    """Endpoint для загрузки файлов из твита.

    HTTP-Params:
        api-key: str
        form-data:
        - file: binary
        - tweet_id: int

    Parameters:
        tweet_id: form-data (int)
        file: FastAPI.UploadFile
        session: Async session
        s3_client: Async client for work with s3 storage

    Returns:
        JSONResponse: результат загрузки файла и идентификатором медиа.
    """
    check_tweet_exist: ResponseData = await TweetsMethods.get(
        tweet_id=tweet_id, async_session=session,
    )
    if not check_tweet_exist.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_tweet_exist.response),
            status_code=check_tweet_exist.status_code,
        )

    media_upload_result: ResponseData = await s3_client.upload(
        file_obj=file.file, filename=file.filename,
    )
    if not media_upload_result.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(media_upload_result.response),
            status_code=media_upload_result.status_code,
        )

    save_link_result: ResponseData = await MediasMethods.add(
        tweet_id=tweet_id,
        link=media_upload_result.response["link"],
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(save_link_result.response),
        status_code=save_link_result.status_code,
    )
