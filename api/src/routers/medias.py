from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/api/medias",
)


@router.post("")
async def upload_media_from_post():
    """
    Endpoint для загрузки файлов из твита. Загрузка происходит через
    отправку формы:

    :HTTP-Params:
        api-key: str
        form: file=”image.jpg”

    :return: JSON
        {
            "result": true,
            "media_id": int
        }
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True, "media_id": 1}
        ),
        status_code=status.HTTP_201_CREATED,
    )
