from fastapi import APIRouter, HTTPException
from fastapi import status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(
    prefix="/api/tweets",
)


@router.get("/")
async def posts_list():
    """
    Returns list of posts for user

    :HTTP-Params:
        api-key: str

    :return: JSON
        {
            "result": true,
            "tweet": [
                {
                    "id": int,
                    "content": string,
                    "attachments": [
                        link_1, // relative?
                        link_2,
                        ...
                    ],
                    "author": {
                        "id": int,
                        "name": string
                    },
                    "likes": [
                        {
                            "user_id": int,
                            "name": string,
                        },
                    ],
                },
                ...,
            ]
        }
    """
    test_json = {
            "result": True,
            "tweet": [
                {
                    "id": int,
                    "content": "string",
                    "attachments": [
                        "link_1",
                        "link_2",
                    ],
                    "author": {
                        "id": 1,
                        "name": "string"
                    },
                    "likes": [
                        {
                            "user_id": 1,
                            "name": "string",
                        },
                    ],
                },
            ]
        }
    return JSONResponse(
        content=jsonable_encoder(test_json),
        status_code=status.HTTP_201_CREATED,
    )


@router.post("/")
async def add_new_post():
    """
    Creates a new post.

    :HTTP-Params:
        api-key: str

    :param: JSON
        {
            "tweet_data": str,
            "tweet_media_ids": Array[int]  # optional
        }

    :return: JSON
        {
            "result": true,
            "tweeet_id": int
        }
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True, "tweeet_id": 1}
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{post_id}")
async def delete_post(post_id: int):
    """
    Deletes the post.

    :HTTP-Params:
        api-key: str

    :param post_id: int

    :return: JSON
        {
            “result”: true
        }

    Note: make sure users delete their own posts!
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True}
        ),
        status_code=status.HTTP_202_ACCEPTED,
    )


@router.post("/{post_id}/likes")
async def like_post(post_id: int):
    """
    Likes the post.

    :HTTP-Params:
        api-key: str

    :param post_id: int

    :return: JSON
        {
            “result”: true
        }
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True}
        ),
        status_code=status.HTTP_201_CREATED,
    )


@router.delete("/{post_id}/likes")
async def remove_like_from_the_post(post_id: int):
    """
    Unlikes the post.

    :HTTP-Params:
        api-key: str

    :param post_id: int

    :return: JSON
        {
            “result”: true
        }
    """
    return JSONResponse(
        content=jsonable_encoder(
            {"result": True}
        ),
        status_code=status.HTTP_201_CREATED,
    )
