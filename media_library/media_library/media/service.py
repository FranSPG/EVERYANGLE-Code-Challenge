from typing import List

from . import model
from media_library.user.model import User
from media_library.auth.jwt import get_current_user


async def get_media_by_id(media_id, database) -> model.Media:
    return database.query(model.Media).filter(model.Media.id == int(media_id)).first()


async def delete_media(form, database):
    media_id = form.get('media_id')
    media = database.query(model.Media).filter(model.Media.id == media_id).delete()
    database.commit()
    return media


async def create_new_media(request, database, current_user) -> model.Media:
    user = database.query(User).filter(User.email == current_user.email).first()
    new_media = model.Media(name=request.media.name, created_date=request.media.created_date,
                            added_date=request.media.added_date, description=request.media.description,
                            genre=request.media.genre, estimated_budget=request.media.estimated_budget,
                            adult=request.media.adult, original_language=request.media.original_language,
                            category_name=request.media.category_name, user_id=user.id)
    database.add(new_media)
    database.commit()
    database.refresh(new_media)
    return new_media


async def create_new_movie(request, database, current_user) -> model.Movie:
    new_media = await create_new_media(request, database, current_user)
    new_movie = model.Movie(
        main_actors=request.main_actors, id_imdb=request.id_imdb,
        product_company_name=request.product_company_name, media_id=new_media.id
    )
    database.add(new_movie)
    database.commit()
    database.refresh(new_movie)
    return new_movie


async def create_new_song(request, database, current_user) -> model.Song:
    new_media = await create_new_media(request, database, current_user)
    new_song = model.Song(
        band_name=request.band_name, disk_name=request.disk_name,
        duration=request.duration,
        media_id=new_media.id)
    database.add(new_song)
    database.commit()
    database.refresh(new_song)
    return new_song


async def create_new_game(request, database, current_user) -> model.Game:
    new_media = await create_new_media(request, database, current_user)
    new_game = model.Game(
        platform=request.platform, publisher=request.publisher,
        is_free=request.is_free, game_category=request.game_category,
        est_playable_minutes=request.est_playable_minutes,
        media_id=new_media.id)
    database.add(new_game)
    database.commit()
    database.refresh(new_game)
    return new_game


async def get_user(database, current_user) -> User:
    return database.query(User).filter(User.email == current_user.email).first()


async def get_all_movies(database, current_user) -> List[model.Movie]:
    user = await get_user(database, current_user)
    media_ids = database.query(model.Media.id).filter(model.Media.user_id == user.id).all()
    media_ids = [media_id[0] for media_id in media_ids]
    movies = database.query(model.Movie).filter(model.Movie.media_id.in_(media_ids)).all()
    return movies


async def get_all_songs(database, current_user) -> List[model.Song]:
    user = await get_user(database, current_user)
    media_ids = database.query(model.Media.id).filter(model.Media.user_id == user.id).all()
    media_ids = [media_id[0] for media_id in media_ids]
    songs = database.query(model.Song).filter(model.Song.media_id.in_(media_ids)).all()
    return songs


async def get_all_games(database, current_user) -> List[model.Game]:
    user = await get_user(database, current_user)
    media_ids = database.query(model.Media.id).filter(model.Media.user_id == user.id).all()
    media_ids = [media_id[0] for media_id in media_ids]
    games = database.query(model.Game).filter(model.Game.media_id.in_(media_ids)).all()
    return games


async def update_media(form, database):
    media = database.query(model.Media).filter(model.Media.id == form.get('media_id'))
    data_to_update = form.__dict__['_dict']
    data_to_update['id'] = data_to_update['media_id']
    data_to_update.pop('media_id')
    data_to_update['adult'] = bool(data_to_update['adult'])
    media.update(data_to_update)
    database.commit()
