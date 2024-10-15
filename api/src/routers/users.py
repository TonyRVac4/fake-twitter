from fastapi import APIRouter, status  # HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(
    prefix="/api/users",
)


@router.post("/{user_id}/follow")
async def follow_user(user_id: int):
    """Follow the user.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int

    Returns:
        JSONResponse: результат выполнения опереации.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{user_id}/follow")
async def unfollow_user(user_id: int):
    """Unfollow the user.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int

    Returns:
        JSONResponse: результат выполнения опереации.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.get("/me")
async def self_profile_info():
    """Return user's profile information.

    HTTP-Params:
        api-key: str

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


@router.get("/{user_id}")
async def user_profile_info_by_id(user_id: int):
    """Return user's profile information.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int

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
