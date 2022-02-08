import pytest
from httpx import AsyncClient

from conf_test_db import app

from media_library.auth.jwt import create_access_token


@pytest.mark.asyncio
async def test_new_movie():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        user_access_token = create_access_token({"sub": "john@gmail.com"})
        payload = {
            "media":
                {
                    "name": "This is a song",
                    "created_date": "2022-02-07",
                    "added_date": "2022-02-07",
                    "description": "This a song",
                    "genre": "Rock",
                    "estimated_budget": 10.0,
                    "adult": True,
                    "original_language": "English",
                    "category_name": "movies"
                },
            "main_actors": "Mark Hamill",
            "id_imdb": 1111,
            "product_company_name": "Disney"}
    response = await ac.post("/media/movies/", json=payload, headers={'Authorization': f'Bearer {user_access_token}'})
    assert response.status_code == 201
    assert response.json()['id_imdb'] == 1111
    assert response.json()['product_company_name'] == "Disney"
    assert response.json()['main_actors'] == "Mark Hamill"
