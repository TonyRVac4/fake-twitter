from httpx import AsyncClient

url = "/api/tweets"


async def test_get_list_of_posts(ac: AsyncClient):
    """Test GET /api/tweets endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(url,
                           headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"}
                           )
    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_create_new_post(ac: AsyncClient):
    """Test POST /api/medias endpoint works.

    Parameters:
        ac: AsyncClient
    """
    test_data: dict = {"tweet_data": "string", "tweet_media_ids": [0, 1]}

    request = await ac.post(url,
                            json=test_data,
                            headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"}
                            )
    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_delete_post(ac: AsyncClient):
    """Test DELETE /api/medias/post_id endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(url + "/{post_id}".format(post_id=1),
                              headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"}
                              )

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_like_post(ac: AsyncClient):
    """Test POST /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(url + "/{post_id}/likes".format(post_id=2),
                            headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"}
                            )
    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_unlike_post(ac: AsyncClient):
    """Test DELETE /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(url + "/{post_id}/likes".format(post_id=2),
                              headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"}
                              )
    assert request.status_code == 200
    assert request.json().get("result") is True
