from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from database_models.db_config import ResponseData, get_async_session
from database_models.methods.users import CookiesMethods


async def api_key_check_dependency(
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    # """Global dependency that act like middleware for validating API key.
    #
    # Parameters:
    #     request: FastAPI.request
    #     session: AsyncSession dependency (get_async_session)
    #
    # Raises:
    #     HTTPException: Unauthorized
    # """
    # api_key: str = request.headers.get("api-key")
    # if not api_key:
    #     raise HTTPException(
    #         detail={
    #             "result": False,
    #             "error_message": "API key's missing",
    #             "error_type": "Unauthorized",
    #         },
    #         status_code=401,
    #     )
    #
    # check_api_key: ResponseData = await CookiesMethods.get_user_id(api_key, session)
    # if not check_api_key.response["result"]:
    #     raise HTTPException(
    #         detail=check_api_key.response,
    #         status_code=check_api_key.status_code,
    #     )
    #
    # # Attach user_id to request.state
    request.state.user_id = 1
