import pytest
from httpx import AsyncClient


url = "/api/tweets"


async def test_get_list_of_posts(ac: AsyncClient):
    request = await ac.get(url)

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_create_new_post(ac: AsyncClient):
    test_data = {}

    request = await ac.post(url, data=test_data)

    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_delete_post(ac:AsyncClient):
    request = await ac.delete(url + "/{post_id}".format(post_id=1))

    assert request.status_code == 202
    assert request.json().get("result") is True


async def test_like_post(ac:AsyncClient):
    request = await ac.post(url + "/{post_id}/likes".format(post_id=1))

    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_unlike_post(ac: AsyncClient):
    request = await ac.delete(url + "/{post_id}/likes".format(post_id=1))

    assert request.status_code == 201
    assert request.json().get("result") is True
