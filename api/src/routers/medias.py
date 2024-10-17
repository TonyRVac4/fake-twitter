from fastapi import APIRouter, status  # HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas import MediaUploadResponseDataWithId

router = APIRouter(
    prefix="/api/medias",
)


@router.post("", response_model=MediaUploadResponseDataWithId)
async def upload_media_from_post():
    """Endpoint для загрузки файлов из твита.

    HTTP-Params:
        api-key: str
        form: file=”image.jpg”

    Returns:
        JSONResponse: результат загрузки файла и идентификатором медиа.
    """
    return JSONResponse(
        content=jsonable_encoder({"result": True, "media_id": 1}),
        status_code=status.HTTP_201_CREATED,
    )
