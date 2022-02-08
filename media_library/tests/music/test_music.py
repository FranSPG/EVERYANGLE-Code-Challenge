import pytest
from httpx import AsyncClient

from conf_test_db import app

from media_library.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_new_music():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "john@gmail.com"})
        payload = {
            "media": {
                "name": "string",
                "created_date": "2022-02-08",
                "added_date": "2022-02-08",
                "description": "string",
                "genre": "string",
                "estimated_budget": 0,
                "adult": False,
                "original_language": "string",
                "category_name": "music"
            },
            "band_name": "This is a band",
            "disk_name": "The disk",
            "duration": 10
        }
    response = await ac.post("/media/songs/", json=payload, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    assert response.json()['band_name'] == "This is a band"
    assert response.json()['disk_name'] == "The disk"
    assert response.json()['duration'] == 10
