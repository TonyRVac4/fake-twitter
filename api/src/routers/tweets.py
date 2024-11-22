from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from types_aiobotocore_s3 import Client
from schemas import BaseResponseDataOut, TweetDataIn, TweetResponseWithId  # noqa
from database_models.db_config import ResponseData, get_async_session  # noqa
from database_models.methods.tweets import LikesMethods, TweetsMethods  # noqa
from database_models.methods.users import CookiesMethods  # noqa
from database_models.methods.medias import MediasMethods  # noqa
from utils.s3_config import get_async_s3_client, S3utils # noqa

router = APIRouter(
    prefix="/api/tweets",
)


@router.get("")
async def posts_list(
    request: Request, session: AsyncSession = Depends(get_async_session),
):
    """Return list of posts for user.

    HTTP-Params:
        api-key: str

    Parameters:
        request: FastAPI Request object
        session: dependency - Async session

    Returns:
        JSON: результат запроса и список словорей с постами.
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

    tweets_data: ResponseData = await TweetsMethods.get_posts_for_user(
        user_id=check_api_key.response["user_id"],
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(tweets_data.response),
        status_code=tweets_data.status_code,
    )


@router.post("", response_model=TweetResponseWithId)
async def add_new_post(
    new_tweet_data: TweetDataIn,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new post.

    HTTP-Params:
        api-key: str

    Parameters:
        new_tweet_data: JSON new tweet data
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат создания поста и идентификатор поста.
    """
    new_tweet: dict = new_tweet_data.model_dump()
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key.response["result"]:
        return JSONResponse(
            content=jsonable_encoder(check_api_key.response),
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await TweetsMethods.add(
        user_id=check_api_key.response["user_id"],
        text=new_tweet["tweet_data"],
        async_session=session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.delete("/{post_id}", response_model=BaseResponseDataOut)
async def delete_post(
    post_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
    s3_client: Client = Depends(get_async_s3_client),
):
    """Delete the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        request: FastAPI Request object
        session: Async session
        s3_client: Async client for work with s3 storage

    Returns:
        JSONResponse: результат удаления поста
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

    get_tweet_media: ResponseData = await MediasMethods.get_by_tweet_id(
        tweet_id=post_id, async_session=session,
    )
    del_from_db_res: ResponseData = await TweetsMethods.delete(
        user_id=check_api_key.response["user_id"],
        tweet_id=post_id,
        async_session=session,
    )
    if del_from_db_res.response["result"] and get_tweet_media.response["links"]:
        file_names: list = [
            S3utils.get_name_from_link(link)
            for link in get_tweet_media.response["links"]
        ]
        await s3_client.delete_multiple(media_names=file_names)
    return JSONResponse(
        content=jsonable_encoder(del_from_db_res.response),
        status_code=del_from_db_res.status_code,
    )


@router.post("/{post_id}/likes", response_model=BaseResponseDataOut)
async def like_post(
    post_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Like the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат установления лайка.
    """
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key:
        return JSONResponse(
            content=check_api_key.response,
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await LikesMethods.add(
        check_api_key.response["user_id"], post_id, session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )


@router.delete("/{post_id}/likes", response_model=BaseResponseDataOut)
async def remove_like_from_the_post(
    post_id: int,
    request: Request,
    session: AsyncSession = Depends(get_async_session),
):
    """Unlike the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int
        request: FastAPI Request object
        session: Async session

    Returns:
        JSONResponse: результат удаления лайка.
    """
    api_key: str = request.headers.get("api-key")
    check_api_key: ResponseData = await CookiesMethods.get_user_id(
        api_key, session,
    )
    if not check_api_key:
        return JSONResponse(
            content=check_api_key.response,
            status_code=check_api_key.status_code,
        )

    result: ResponseData = await LikesMethods.delete(
        check_api_key.response["user_id"], post_id, session,
    )
    return JSONResponse(
        content=jsonable_encoder(result.response),
        status_code=result.status_code,
    )
