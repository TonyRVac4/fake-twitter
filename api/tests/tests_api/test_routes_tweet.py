from httpx import AsyncClient

url = "/api/tweets"


async def test_get_list_of_posts(ac: AsyncClient):
    """Test GET /api/tweets endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(url)

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_create_new_post(ac: AsyncClient):
    """Test POST /api/medias endpoint works.

    Parameters:
        ac: AsyncClient
    """
    test_data: dict = {"tweet_data": "string", "tweet_media_ids": [0, 1, 54]}

    request = await ac.post(url, json=test_data)
    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_delete_post(ac: AsyncClient):
    """Test DELETE /api/medias/post_id endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(url + "/{post_id}".format(post_id=1))

    assert request.status_code == 202
    assert request.json().get("result") is True


async def test_like_post(ac: AsyncClient):
    """Test POST /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(url + "/{post_id}/likes".format(post_id=1))

    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_unlike_post(ac: AsyncClient):
    """Test DELETE /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(url + "/{post_id}/likes".format(post_id=1))

    assert request.status_code == 201
    assert request.json().get("result") is True
