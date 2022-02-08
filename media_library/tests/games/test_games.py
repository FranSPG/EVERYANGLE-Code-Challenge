import pytest
from httpx import AsyncClient

from conf_test_db import app

from media_library.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_new_game():
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
                "category_name": "games"
            },
            "platform": "PS5",
            "publisher": "Activision",
            "is_free": True,
            "game_category": "Action",
            "est_playable_minutes": 10
        }
    response = await ac.post("/media/games/", json=payload, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    assert response.json()['platform'] == "PS5"
    assert response.json()['publisher'] == "Activision"
    assert response.json()['is_free'] is True
    assert response.json()['game_category'] == "Action"
    assert response.json()['est_playable_minutes'] == 10
