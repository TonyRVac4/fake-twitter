from httpx import AsyncClient


async def test_media_upload(ac: AsyncClient):
    """Test /api/medias endpoint works.

    Parameters:
        ac: AsyncClient
    """
    test_data: dict = {}

    request = await ac.post("/api/medias", data=test_data)

    assert request.status_code == 201
    assert request.json().get("result") is True
