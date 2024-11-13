from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database_models.db_config import ResponseData, get_async_session  # noqa
from database_models.methods.users import UsersMethods  # noqa
from database_models.methods.users import CookiesMethods, FollowersMethods # noqa
from schemas import BaseResponseDataOut, UserProfileDataOut  # noqa

router = APIRouter(
    prefix="/api/users",
)


@router.post("/{user_id}/follow", response_model=BaseResponseDataOut)
async def follow_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Follow the user.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат выполнения опереации.
    """
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await FollowersMethods.add(
        follower_id=check_api_key.response["user_id"],
        following_id=user_id,
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.delete("/{user_id}/follow", response_model=BaseResponseDataOut)
async def unfollow_user(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Unfollow the user.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат выполнения опереации.
    """
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await FollowersMethods.delete(
        follower_id=check_api_key.response["user_id"],
        following_id=user_id,
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.get("/me", response_model=UserProfileDataOut)
async def self_profile_info(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Return user's profile information.

    HTTP-Params:
        api-key: str

    Parameters:
        request: FastAPI Request object
        session: Async session

    Returns:
        JSON: результат запроса и информацию о пользователе.
    """
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await UsersMethods.get_info_by_id(
        user_id=check_api_key.response["user_id"],
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.get("/{user_id}", response_model=UserProfileDataOut)
async def user_profile_info_by_id(
    user_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Return user's profile information.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат запроса и информацию о пользователе.
    """
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await UsersMethods.get_info_by_id(
        user_id=user_id,
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )
