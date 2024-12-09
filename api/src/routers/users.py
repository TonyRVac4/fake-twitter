from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_cache.decorator import cache
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
    follower_id = request.state.user_id

    result: ResponseData = await FollowersMethods.add(
        follower_id=follower_id,
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
    follower_id = request.state.user_id

    result: ResponseData = await FollowersMethods.delete(
        follower_id=follower_id,
        following_id=user_id,
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.get("/me", response_model=UserProfileDataOut)
@cache(expire=30)
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
    user_id = request.state.user_id

    result: ResponseData = await UsersMethods.get_info_by_id(
        user_id=user_id,
        async_session=session,
    )
    if not result.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(result.response),
            status_code=result.status_code,
        )
    return jsonable_encoder(result.response)


@router.get("/{user_id}", response_model=UserProfileDataOut)
@cache(expire=30)
async def user_profile_info_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Return user's profile information.

    HTTP-Params:
        api-key: str

    Parameters:
        user_id: int
        session: Async session

    Returns:
        JSONResponse: результат запроса и информацию о пользователе.
    """
    result: ResponseData = await UsersMethods.get_info_by_id(
        user_id=user_id,
        async_session=session,
    )
    if not result.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(result.response),
            status_code=result.status_code,
        )
    return jsonable_encoder(result.response)
