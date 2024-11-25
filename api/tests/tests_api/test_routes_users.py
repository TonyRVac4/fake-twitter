from httpx import AsyncClient

url = "/api/users"


async def test_follow_user(ac: AsyncClient):
    """Test POST /api/users/post_id/follow endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(
        url + "/{user_id}/follow".format(user_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_cant_follow_yourself(ac: AsyncClient):
    """Test POST /api/users/post_id/follow can not follow yourself.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(
        url + "/{user_id}/follow".format(user_id=1),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 400
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "ValueError"


async def test_cant_follow_when_already_followed(ac: AsyncClient):
    """Test POST /api/users/post_id/follow.

    Can not follow user that who is already followed.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(
        url + "/{user_id}/follow".format(user_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 400
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "UniqueViolationError"


async def test_cant_follow_nonexistent_user(ac: AsyncClient):
    """Test POST /api/users/post_id/follow.

    Can not follow user that does not exist.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(
        url + "/{user_id}/follow".format(user_id=23),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 404
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "DataNotFound"


async def test_unfollow_user(ac: AsyncClient):
    """Test DELETE /api/users/post_id/follow endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{user_id}/follow".format(user_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 204
    assert request.json().get("result") is True


async def test_cant_unfollow_when_user_is_not_followed(ac: AsyncClient):
    """Test DELETE /api/users/post_id/follow.

    Can not unfollow when user is not followed.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{user_id}/follow".format(user_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 404
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "DataNotFound"


async def test_get_self_profile_info(ac: AsyncClient):
    """Test GET /api/users/me endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(
        "".join([url, "/me"]),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_get_profile_info_by_id(ac: AsyncClient):
    """Test GET /api/users/user_id endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(
        url + "/{user_id}".format(user_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_cant_get_user_data_of_nonexistent_user(ac: AsyncClient):
    """Test GET /api/users/user_id.

    Can not get user data by id that does not exist.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(
        url + "/{user_id}".format(user_id=22),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 404
    assert request.json().get("result") is False
