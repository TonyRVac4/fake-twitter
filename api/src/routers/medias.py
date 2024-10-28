from fastapi import APIRouter, status, Depends  # HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import MediaUploadResponseDataWithId
from database_models.db_config import get_async_session

router = APIRouter(
    prefix="/api/medias",
)


@router.post("", response_model=MediaUploadResponseDataWithId)
async def upload_media_from_post(session: AsyncSession = Depends(get_async_session)):
    """Endpoint для загрузки файлов из твита.

    HTTP-Params:
        api-key: str
        form: file=”image.jpg”
    Parameters:
        session: Async session
    Returns:
        JSONResponse: результат загрузки файла и идентификатором медиа.
    """
    return JSONResponse(
        content=jsonable_encoder({"result": True, "media_id": 1}),
        status_code=status.HTTP_201_CREATED,
    )
