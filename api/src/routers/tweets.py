from fastapi import APIRouter, status, Depends, Request
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from schemas import BaseResponseDataOut, TweetDataIn, TweetResponseWithId

from database_models.methods.tweets import TweetsMethods
from database_models.methods.users import CookiesMethods
from database_models.db_config import get_async_session, ResponseData

router = APIRouter(
    prefix="/api/tweets",
)


@router.get("")
async def posts_list(request: Request, session: AsyncSession = Depends(get_async_session)):
    """Return list of posts for user.

    HTTP-Params:
        api-key: str

    Parameters:
        request: FastAPI Request object
        session: dependency - Async session

    Returns:
        JSON: результат запроса и список словорей с постами.
    """

    check_api_key: ResponseData = await CookiesMethods.get_user_id(request.headers.get("api-key"), session)
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    tweets_data: ResponseData = await TweetsMethods.get_all(check_api_key.response["user_id"], session)
    return JSONResponse(
        content=jsonable_encoder(tweets_data.response),
        status_code=tweets_data.status_code,
    )


@router.post("", response_model=TweetResponseWithId)
async def add_new_post(new_tweet_data: TweetDataIn, request: Request, session: AsyncSession = Depends(get_async_session)):
    """Create a new post.

    HTTP-Params:
        api-key: str

    Parameters:
        new_tweet_data: JSON текст поста и опциональный список
                        идентификаторов медиа файлов.
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат создания поста и идентификатор поста.

    """
    new_tweet: dict = new_tweet_data.dict()

    check_api_key: ResponseData = await CookiesMethods.get_user_id(request.headers.get("api-key"), session)
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await TweetsMethods.add(check_api_key.response["user_id"], new_tweet, session)
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.delete("/{post_id}", response_model=BaseResponseDataOut)
async def delete_post(post_id: int, request: Request, session: AsyncSession = Depends(get_async_session)):
    """Delete the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат удаления поста
    """
    check_api_key: ResponseData = await CookiesMethods.get_user_id(request.headers.get("api-key"), session)
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await TweetsMethods.delete(
        user_id=check_api_key.response["user_id"],
        tweet_id=post_id,
        async_session=session
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.post("/{post_id}/likes", response_model=BaseResponseDataOut)
async def like_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    """Like the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        session: Async session

    Returns:
        JSONResponse: результат установления лайка.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{post_id}/likes", response_model=BaseResponseDataOut)
async def remove_like_from_the_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    """Unlike the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        session: Async session

    Returns:
        JSONResponse: результат удаления лайка.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_201_CREATED,
    )
