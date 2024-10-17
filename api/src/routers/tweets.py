from fastapi import APIRouter, status  # HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from schemas import BaseResponseDataOut, TweetDataIn, TweetResponseWithId

router = APIRouter(
    prefix="/api/tweets",
)


@router.get("")
async def posts_list():
    """Return list of posts for user.

    HTTP-Params:
        api-key: str

    Returns:
        JSON: результат запроса и список словорей с постами.
    """
    test_json = {
        "result": True,
        "tweet": [
            {
                "id": 1,
                "content": "string",
                "attachments": [
                    "link_1",
                    "link_2",
                ],
                "author": {
                    "id": 1,
                    "name": "string",
                },
                "likes": [
                    {
                        "user_id": 1,
                        "name": "string",
                    },
                ],
            },
        ],
    }
    return JSONResponse(
        content=jsonable_encoder(test_json),
        status_code=status.HTTP_200_OK,
    )


@router.post("", response_model=TweetResponseWithId)
async def add_new_post(new_tweet_data: TweetDataIn):
    """Create a new post.

    HTTP-Params:
        api-key: str

    Parameters:
        new_tweet_data: JSON текст поста и опциональный список
                        идентификаторов медиа файлов.

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
async def delete_post(post_id: int):
    """Delete the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int

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
async def like_post(post_id: int):
    """Like the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int

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
async def remove_like_from_the_post(post_id: int):
    """Unlike the post.

    HTTP-Params:
        api-key: str

    Parameters:
        post_id: int

    Returns:
        JSONResponse: результат удаления лайка.
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True},
        ),
        status_code=status.HTTP_201_CREATED,
    )
