from typing import List

from fastapi import HTTPException, status

from . import model


async def create_new_category(request, database) -> model.Category:
    new_category = model.Category(name=request.name)
    database.add(new_category)
    database.commit()
    database.refresh(new_category)
    return new_category


async def get_all_categories(database) -> List[model.Category]:
    categories = database.query(model.Category).all()
    return categories


async def get_category_by_id(category_id, database) -> model.Category:
    category_info = database.query(model.Category).get(category_id)
    if not category_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Data Not Found !")
    return category_info


async def delete_category_by_id(category_id, database):
    database.query(model.Category).filter(model.Category.id == category_id).delete()
    database.commit()


async def create_new_media(request, category_id, database) -> model.Media:
    new_media = model.Media(name=request.media.name, created_date=request.media.created_date,
                            added_date=request.media.added_date, description=request.media.description,
                            genre=request.media.genre, estimated_budget=request.media.estimated_budget,
                            adult=request.media.adult, original_language=request.media.original_language,
                            category_id=category_id)
    database.add(new_media)
    database.commit()
    database.refresh(new_media)
    return new_media


async def create_new_movie(request, category_id, database) -> model.Movie:
    new_media = await create_new_media(request, category_id, database)
    new_movie = model.Movie(
        main_actors=request.main_actors, id_imdb=request.id_imdb,
        product_company_name=request.product_company_name, media_id=new_media.id
    )
    database.add(new_movie)
    database.commit()
    database.refresh(new_movie)
    return new_movie


async def create_new_song(request, category_id, database) -> model.Song:
    new_media = await create_new_media(request, category_id, database)
    new_song = model.Song(
        band_name=request.band_name, disk_name=request.disk_name,
        duration=request.duration,
        media_id=new_media.id)
    database.add(new_song)
    database.commit()
    database.refresh(new_song)
    return new_song


async def create_new_game(request, category_id, database) -> model.Game:
    new_media = await create_new_media(request, category_id, database)
    new_game = model.Game(
        platform=request.platform, publisher=request.publisher,
        is_free=request.is_free, game_category=request.game_category,
        est_playable_minutes=request.est_playable_minutes,
        media_id=new_media.id)
    database.add(new_game)
    database.commit()
    database.refresh(new_game)
    return new_game


async def get_all_movies(database) -> List[model.Movie]:
    movies = database.query(model.Movie).all()
    return movies


async def get_all_songs(database) -> List[model.Song]:
    songs = database.query(model.Song).all()
    return songs


async def get_all_games(database) -> List[model.Game]:
    games = database.query(model.Game).all()
    return games
