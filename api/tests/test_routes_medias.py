import pytest
from httpx import AsyncClient


async def test_media_upload(ac: AsyncClient):
    test_data = {}

    request = await ac.post("/api/medias", data=test_data)

    assert request.status_code == 201
    assert request.json().get("result") is True
