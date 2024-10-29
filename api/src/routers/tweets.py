from fastapi import APIRouter, status, Depends, Request  # HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from schemas import BaseResponseDataOut, TweetDataIn, TweetResponseWithId

from database_models.methods.tweets import TweetsMethods
from database_models.methods.users import CookiesMethods
from database_models.db_config import get_async_session

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

    check_api_key: dict = await CookiesMethods.get_user_id(request.headers.get("api-key"), session)
    if check_api_key["result"] is False:
        return JSONResponse(
            content=jsonable_encoder(check_api_key),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    tweets_data: dict = await TweetsMethods.get_all(check_api_key["user_id"], session)
    if tweets_data["result"] is True:
        return JSONResponse(
            content=jsonable_encoder(tweets_data),
            status_code=status.HTTP_200_OK,
        )
    return JSONResponse(
        content=jsonable_encoder(tweets_data),
        status_code=status.HTTP_404_NOT_FOUND,
    )


@router.post("", response_model=TweetResponseWithId)
async def add_new_post(new_tweet_data: TweetDataIn, session: AsyncSession = Depends(get_async_session)):
    """Create a new post.

    HTTP-Params:
        api-key: str

    Parameters:
        new_tweet_data: JSON текст поста и опциональный список
                        идентификаторов медиа файлов.
        session: Async session

    Returns:
        JSONResponse: результат создания поста и идентификатор поста.

    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True, "tweeet_id": 1},
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{post_id}", response_model=BaseResponseDataOut)
async def delete_post(post_id: int, session: AsyncSession = Depends(get_async_session)):
    """Delete the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        session: Async session

    Returns:
        JSONResponse: результат удаления поста

    Note: make sure users delete their own posts!
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_202_ACCEPTED,
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
