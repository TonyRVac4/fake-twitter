from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, Header
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_s3 import Client
from database_models.db_config import get_async_session  # noqa
from utils.s3_config import get_async_s3_client # noqa
from schemas import MediaUploadResponseDataWithId  # noqa

from database_models.db_config import ResponseData, get_async_session  # noqa
from database_models.methods.medias import MediasMethods  # noqa
from database_models.methods.users import CookiesMethods, FollowersMethods # noqa
from schemas import BaseResponseDataOut  # noqa

router = APIRouter(
    prefix="/api/medias",
)


@router.post("", response_model=MediaUploadResponseDataWithId)
async def upload_media_from_post(
    tweet_id: Annotated[int, Form()],
    file: UploadFile,
    api_key: Annotated[str, Header()],
    session: AsyncSession = Depends(get_async_session),
    s3_client: Client = Depends(get_async_s3_client),
):
    """Endpoint для загрузки файлов из твита.

    HTTP-Params:
        api-key: str
        form-data:
            file: binary
            tweet_id: int

    Parameters:
        tweet_id: int
        file: FastAPI.UploadFile
        api_key: str
        session: Async session
        s3_client: Async client for work with s3 storage

    Returns:
        JSONResponse: результат загрузки файла и идентификатором медиа.
    """

    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
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
