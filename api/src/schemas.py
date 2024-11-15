from pydantic import BaseModel, ConfigDict


class BaseResponseDataOut(BaseModel):
    """Base class for responses with result status."""

    model_config = ConfigDict(from_attributes=True)

    result: bool


class UserBaseData(BaseModel):
    """Class with basic user info (id, name)."""

    id: int
    name: str


class TweetDataIn(BaseModel):
    """Class for validation incoming new post data."""

    tweet_data: str
    tweet_media_ids: list[int] | None


class TweetResponseWithId(BaseResponseDataOut):
    """Class extends basic response with tweed_id."""

    tweet_id: int


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
