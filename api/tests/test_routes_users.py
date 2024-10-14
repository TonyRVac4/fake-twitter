import pytest
from httpx import AsyncClient


url = "/api/users"


async def test_follow_user(ac: AsyncClient):
    request = await ac.post(url + "/{user_id}/follow".format(user_id=1))

    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_unfollow_user(ac: AsyncClient):
    request = await ac.delete(url + "/{user_id}/follow".format(user_id=1))

    assert request.status_code == 202
    assert request.json().get("result") is True


async def test_get_self_profile_info(ac: AsyncClient):
    request = await ac.get(url + "/me")

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_get_profile_info_by_id(ac: AsyncClient):
    request = await ac.get(url + "/{user_id}".format(user_id=1))

    assert request.status_code == 200
    assert request.json().get("result") is True
