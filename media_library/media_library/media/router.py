from typing import List
from ast import literal_eval

from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlalchemy.orm import Session

from media_library import db
from . import schema
from . import service
from . import validator
from media_library.auth.jwt import get_current_user
from media_library.user.schema import User
from fastapi.responses import RedirectResponse

from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

router = APIRouter(
    tags=['Media'],
    prefix='/media'
)

templates = Jinja2Templates(directory="static/templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.post('/update_media')
async def update_media(request: Request, database: Session = Depends(db.get_db)):
    """
    Takes a media coming in the request form and updates the object in the database.
    :param request: Update form.
    :param database: Session of the database.
    :return: Renders the home directory with the data updated.
    """
    form = await request.form()
    await service.update_media(form, database)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return resp


@router.get('/update_media')
async def update_media(request: Request):
    """
    It renders the update_media.html where all the fields are filled up with the data of a specific media.
    :param request: data of the media.
    :return: renders the template with the data of the media.
    """
    data = literal_eval(request.cookies.get('data'))
    return templates.TemplateResponse("media/update_media.html",
                                      {"request": data})


@router.post('/update_media_get_id')
async def update_media_get_id(request: Request, database: Session = Depends(db.get_db)):
    """
    Takes the media id input from the user.
    :param request: form that contains the media id.
    :param database: Session of the database.
    :return: Renders the update_media with the data of the media filled up.
    """
    token = request.cookies.get("access_token")
    current_user: User = get_current_user(token)
    form = await request.form()
    media = await service.get_media_by_id(form.get('media_id'), database)
    resp = RedirectResponse(url='/media/update_media', status_code=status.HTTP_302_FOUND)
    resp.delete_cookie('data')
    media.__dict__.pop("_sa_instance_state")
    media.__dict__.pop("added_date")
    media.__dict__.pop("created_date")
    media.__dict__['media_id'] = form.get('media_id')
    resp.set_cookie("data", media.__dict__)
    return resp


@router.get('/update_media_get_id')
async def update_media_get(request: Request):
    return templates.TemplateResponse("media/update_media_get_id.html",
                                      {"request": request})


@router.post('/delete_media')
async def delete_media_get(request: Request, database: Session = Depends(db.get_db)):
    """
    Deletes a media given an id.
    :param request: Form that contains a media id.
    :param database: Session of the database.
    :return: Redirects to the home with the data updated.
    """
    token = request.cookies.get("access_token")
    current_user: User = get_current_user(token)
    form = await request.form()
    await service.delete_media(form, database)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return resp


@router.get('/delete_media')
async def delete_media_get(request: Request):
    return templates.TemplateResponse("media/delete_media.html",
                                      {"request": request})


@router.get('/movies')
async def create_movie_get(request: Request):
    return templates.TemplateResponse("media/create_movie.html",
                                      {"request": request})


@router.get('/songs')
async def create_song_get(request: Request):
    return templates.TemplateResponse("media/create_song.html",
                                      {"request": request})


@router.get('/games')
async def create_game_get(request: Request):
    return templates.TemplateResponse("media/create_game.html",
                                      {"request": request})


@router.post('/movies', status_code=status.HTTP_201_CREATED)
async def create_movie(request: Request, database: Session = Depends(db.get_db)):
    """
    Creates a media and a movie object in the database.
    :param request: Form with the media and movie data.
    :param database: Session of the database.
    :return: Redirects to the home page.
    """
    token = request.cookies.get("access_token")
    current_user: User = get_current_user(token)
    form = await request.form()
    media = schema.MediaBase(
        name=form.get('name'),
        created_date=form.get('created_date'),
        added_date=form.get('added_date'),
        description=form.get('description'),
        genre=form.get('genre'),
        estimated_budget=form.get('estimated_budget'),
        adult=form.get('adult'),
        original_language=form.get('original_language'),
        category_name="movies"
    )
    movie = schema.Movie(
        media=media,
        main_actors=form.get('main_actors'),
        id_imdb=form.get('id_imdb'),
        product_company_name=form.get('product_company_name')
    )
    category = await validator.verify_category_exist(media.category_name)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category must be movies, games or music.",
        )
    await service.create_new_movie(movie, database, current_user)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return resp


@router.post('/songs', status_code=status.HTTP_201_CREATED)
async def create_movie(request: Request, database: Session = Depends(db.get_db)):
    token = request.cookies.get("access_token")
    current_user: User = get_current_user(token)
    form = await request.form()
    media = schema.MediaBase(
        name=form.get('name'),
        created_date=form.get('created_date'),
        added_date=form.get('added_date'),
        description=form.get('description'),
        genre=form.get('genre'),
        estimated_budget=form.get('estimated_budget'),
        adult=form.get('adult'),
        original_language=form.get('original_language'),
        category_name="music"
    )
    song = schema.Song(
        media=media,
        band_name=form.get('band_name'),
        disk_name=form.get('disk_name'),
        duration=form.get('duration')
    )
    category = await validator.verify_category_exist(media.category_name)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category must be movies, games or music.",
        )
    await service.create_new_song(song, database, current_user)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return resp


@router.post('/games', status_code=status.HTTP_201_CREATED)
async def create_movie(request: Request, database: Session = Depends(db.get_db)):
    token = request.cookies.get("access_token")
    current_user: User = get_current_user(token)
    form = await request.form()
    media = schema.MediaBase(
        name=form.get('name'),
        created_date=form.get('created_date'),
        added_date=form.get('added_date'),
        description=form.get('description'),
        genre=form.get('genre'),
        estimated_budget=form.get('estimated_budget'),
        adult=form.get('adult'),
        original_language=form.get('original_language'),
        category_name="games"
    )
    game = schema.Game(
        media=media,
        platform=form.get('platform'),
        publisher=form.get('publisher'),
        is_free=form.get('is_free'),
        game_category=form.get('game_category'),
        est_playable_minutes=form.get('est_playable_minutes')
    )
    category = await validator.verify_category_exist(media.category_name)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category must be movies, games or music.",
        )
    await service.create_new_game(game, database, current_user)
    resp = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    return resp


@router.get('/movies', response_model=List[schema.Movie])
async def get_all_movies(database: Session = Depends(db.get_db),
                         current_user: User = Depends(get_current_user)):
    return await service.get_all_movies(database, current_user)


@router.post('/songs', status_code=status.HTTP_201_CREATED)
async def create_song(request: schema.Song, database: Session = Depends(db.get_db),
                      current_user: User = Depends(get_current_user)):
    category = await validator.verify_category_exist(request.media.category_name)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category must be movies, games or music.",
        )

    product = await service.create_new_song(request, database, current_user)
    return product


@router.get('/songs', response_model=List[schema.Song])
async def get_all_songs(database: Session = Depends(db.get_db), current_user: User = Depends(get_current_user)):
    return await service.get_all_songs(database, current_user)


@router.post('/games', status_code=status.HTTP_201_CREATED)
async def create_game(request: schema.Game, database: Session = Depends(db.get_db),
                      current_user: User = Depends(get_current_user)):
    category = await validator.verify_category_exist(request.media.category_name)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category must be movies, games or music.",
        )

    game = await service.create_new_game(request, database, current_user)

    return game


@router.get('/games', response_model=List[schema.Game])
async def get_all_games(database: Session = Depends(db.get_db), current_user: User = Depends(get_current_user)):
    return await service.get_all_games(database, current_user)
