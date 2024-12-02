import os

from httpx import AsyncClient

os.chdir(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


async def test_upload_media_from_post(ac: AsyncClient):
    """Test /api/medias endpoint works.

    Parameters:
        ac: AsyncClient
    """
    with open("tests/medias/cat1.jpg", "rb") as file:
        b_file: bytes = file.read()

    file_data = ("test_image.png", b_file, "image/jpg")

    request = await ac.post(
        url="/api/medias",
        files={"file": file_data},
        headers={"api-key": "1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p"},
    )

    assert request.status_code == 201
    assert request.json().get("result") is True
    assert request.json().get("media_id") is not None
