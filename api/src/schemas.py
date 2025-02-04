from typing import List, Optional, Annotated, Union

from pydantic import BaseModel, ConfigDict
from fastapi import Query


class BaseResponseDataOut(BaseModel):
    """Base class for responses with result status."""

    model_config = ConfigDict(from_attributes=True)

    result: bool


class UserBaseData(BaseModel):
    """Class with basic user info (id, name)."""

    id: int
    name: str


class UserBaseDataV2(BaseModel):
    """Class with basic user info (id, name)."""

    user_id: int
    name: str


class TweetDataIn(BaseModel):
    """Class for validation incoming new post data."""

    tweet_data: str
    tweet_media_ids: list[int] | None


class TweetResponseWithId(BaseResponseDataOut):
    """Class extends basic response with tweed_id."""

    tweet_id: int


class TweetFullData(BaseModel):
    """Class response with full info about tweet."""

    id: int
    content: str
    attachments: List[str]
    author: UserBaseData
    likes: List[UserBaseDataV2]


class TweetsListDataOut(BaseResponseDataOut):
    """Class extends basic response with tweets list."""

    tweets: List[TweetFullData]


class MediaUploadResponseDataWithId(BaseResponseDataOut):
    """Class extends basic response with media_id."""

    media_id: int


class UserData(UserBaseData):
    """Class extends basic user's data with followers and following lists."""

    followers: list[UserBaseData] | None
    following: list[UserBaseData] | None


class UserProfileDataOut(BaseResponseDataOut):
    """Class extends basic response with user's profile data."""

    user: UserData


class Pagination(BaseModel):
    offset: Optional[int]
    limit: Optional[int]


def pagination_params(
    offset: Annotated[Union[int, None], Query(ge=1, le=150)] = None,
    limit: Annotated[Union[int, None], Query(ge=1, le=100)] = None,
):
    return Pagination(offset=offset, limit=limit)
