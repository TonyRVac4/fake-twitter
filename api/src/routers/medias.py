from fastapi import APIRouter, Depends, UploadFile
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


@router.post("", response_model=MediaUploadResponseDataWithId, status_code=201)
async def upload_media_from_post(
    file: UploadFile,
    session: AsyncSession = Depends(get_async_session),
    s3_client: Client = Depends(get_async_s3_client),
):
    """Endpoint для загрузки файлов из твита.

    Parameters:
        file: FastAPI.UploadFile
        session: Async session
        s3_client: Async client for work with s3 storage

    Returns:
        JSONResponse: результат загрузки файла и идентификатором медиа.
    """
    media_upload_result: ResponseData = await s3_client.upload(
        file_obj=file.file, filename=file.filename,
    )
    if not media_upload_result.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(media_upload_result.response),
            status_code=media_upload_result.status_code,
        )

    save_link_result: ResponseData = await MediasMethods.add(
        link=media_upload_result.response["link"],
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(save_link_result.response),
        status_code=save_link_result.status_code,
    )
