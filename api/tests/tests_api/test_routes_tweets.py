from httpx import AsyncClient

url = "/api/tweets"


async def test_get_list_of_posts(ac: AsyncClient):
    """Test GET /api/tweets endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(url, headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"})
    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_request_with_nonexistent_api_key(ac: AsyncClient):
    """Test GET /api/tweets endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(url, headers={"api-key": "bg7b3cbd546f7g8h9i0j1k2l3m4n5o6p"})
    assert request.status_code == 401
    assert request.json().get("detail").get("result") is False
    assert request.json().get("detail").get("error_type") == "Unauthorized"


async def test_request_with_no_api_key(ac: AsyncClient):
    """Test GET /api/tweets endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.get(url)
    assert request.status_code == 401
    assert request.json().get("detail").get("result") is False
    assert request.json().get("detail").get("error_type") == "Unauthorized"


async def test_create_new_post(ac: AsyncClient):
    """Test POST /api/medias endpoint works.

    Parameters:
        ac: AsyncClient
    """
    test_data: dict = {"tweet_data": "string", "tweet_media_ids": [0, 1]}

    request = await ac.post(
        url, json=test_data, headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_delete_post(ac: AsyncClient):
    """Test DELETE /api/medias/post_id endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{post_id}".format(post_id=1),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_cant_delete_other_peoples_tweet(ac: AsyncClient):
    """Test DELETE /api/medias/post_id endpoint.

    Doesn't allow to delete other people's tweets.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{post_id}".format(post_id=3),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 401
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "ActionForbidden"


async def test_cant_delete_nonexistent_tweet(ac: AsyncClient):
    """Test DELETE /api/medias/post_id endpoint.

    Return info that tweet does not exist.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{post_id}".format(post_id=1),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 404
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "DataNotFound"


async def test_like_post(ac: AsyncClient):
    """Test POST /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(
        url + "/{post_id}/likes".format(post_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 201
    assert request.json().get("result") is True


async def test_cant_like_liked_post(ac: AsyncClient):
    """Test POST /api/medias/post_id/likes endpoint.

    Returns info that like already exists.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.post(
        url + "/{post_id}/likes".format(post_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 400
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "UniqueViolationError"


async def test_unlike_post(ac: AsyncClient):
    """Test DELETE /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{post_id}/likes".format(post_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 200
    assert request.json().get("result") is True


async def test_cant_delete_nonexistent_like(ac: AsyncClient):
    """Test POST /api/medias/post_id/likes endpoint works.

    Parameters:
        ac: AsyncClient
    """
    request = await ac.delete(
        url + "/{post_id}/likes".format(post_id=2),
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )
    assert request.status_code == 404
    assert request.json().get("result") is False
    assert request.json().get("error_type") == "DataNotFound"
