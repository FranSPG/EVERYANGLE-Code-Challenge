from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from media_library import db
from media_library.auth.jwt import get_current_user
from media_library.user.schema import User

from media_library.media.service import get_all_songs, get_all_games, get_all_movies

router = APIRouter(
    tags=['Home'],
    prefix=''
)

templates = Jinja2Templates(directory="static/templates")
router.mount("/static", StaticFiles(directory="static"), name="static")


@router.get("/")
async def home(request: Request, database: Session = Depends(db.get_db)):
    """
    If there is a session, it gets all the data of that users and display it in the home page.
    :param request: Request data.
    :param database: Session of the database.
    :return: Renders the home.html template.
    """
    try:
        token = request.cookies.get("access_token")
        current_user: User = get_current_user(token)
        movies = await get_all_movies(database, current_user)
        songs = await get_all_songs(database, current_user)
        games = await get_all_games(database, current_user)
    except:
        current_user = None
        movies = []
        songs = []
        games = []

    movies_list = []
    for movie in movies:
        movies_list.append(movie.media.__dict__)

    songs_list = []
    for song in songs:
        songs_list.append(song.media.__dict__)

    games_list = []
    for game in games:
        games_list.append(game.media.__dict__)

    return templates.TemplateResponse("home/home.html",
                                      {"request": request,
                                       "current_user": current_user,
                                       "movies": movies_list,
                                       "songs": songs_list,
                                       "games": games_list})
