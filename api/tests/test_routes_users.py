from httpx import AsyncClient

url = "/api/users"


async def test_follow_user(ac: AsyncClient):
    """Test POST /api/users/post_id/follow endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(url + "/{user_id}/follow".format(user_id=1))

    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_unfollow_user(ac: AsyncClient):
    """Test DELETE /api/users/post_id/follow endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(url + "/{user_id}/follow".format(user_id=1))

    assert request.status_code == 202
    assert request.json().get("result") is True


async def test_get_self_profile_info(ac: AsyncClient):
    """Test DELETE /api/users/me endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get("".join([url, "/me"]))

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_get_profile_info_by_id(ac: AsyncClient):
    """Test DELETE /api/users/user_id endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(url + "/{user_id}".format(user_id=1))

    assert request.status_code == 200
    assert request.json().get("result") is True
