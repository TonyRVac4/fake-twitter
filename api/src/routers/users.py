from fastapi import APIRouter, status, Depends  # HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import BaseResponseDataOut, UserProfileDataOut
from database_models.db_config import get_async_session

router = APIRouter(
    prefix="/api/users",
)


@router.post("/{user_id}/follow", response_model=BaseResponseDataOut)
async def follow_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """Follow the user.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        session: Async session

    Returns:
        JSONResponse: результат выполнения опереации.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{user_id}/follow", response_model=BaseResponseDataOut)
async def unfollow_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """Unfollow the user.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        session: Async session

    Returns:
        JSONResponse: результат выполнения опереации.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.get("/me", response_model=UserProfileDataOut)
async def self_profile_info(session: AsyncSession = Depends(get_async_session)):
    """Return user's profile information.

    HTTP-Params:
        api-key: str

    Parameters:
        session: Async session

    Returns:
        JSON: результат запроса и информацию о пользователе.
    """
    test_json = {
        "result": True,
        "user": {
            "id": 1,
            "name": "str",
            "followers": [
                {
                    "id": 1,
                    "name": "str",
                },
            ],
            "following": [
                {
                    "id": 1,
                    "name": "str",
                },
            ],
        },
    }
    return JSONResponse(
        content=jsonable_encoder(test_json),
        status_code=status.HTTP_200_OK,
    )


@router.get("/{user_id}", response_model=UserProfileDataOut)
async def user_profile_info_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    """Return user's profile information.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        session: Async session

    Returns:
        JSONResponse: результат запроса и информацию о пользователе.
    """
    test_json = {
        "result": True,
        "user": {
            "id": 1,
            "name": "str",
            "followers": [
                {
                    "id": 1,
                    "name": "str",
                },
            ],
            "following": [
                {
                    "id": 1,
                    "name": "str",
                },
            ],
        },
    }
    return JSONResponse(
        content=jsonable_encoder(test_json),
        status_code=status.HTTP_200_OK,
    )
