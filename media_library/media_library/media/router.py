from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from media_library import db
from . import schema
from . import service
from . import validator
from media_library.auth.jwt import get_current_user
from media_library.user.schema import User

router = APIRouter(
    tags=['Media'],
    prefix='/media'
)


@router.post('/movies', status_code=status.HTTP_201_CREATED)
async def create_movie(request: schema.Movie, database: Session = Depends(db.get_db),
                       current_user: User = Depends(get_current_user)):
    category = await validator.verify_category_exist(request.media.category_name)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="Category must be movies, games or music.",
        )
    movie = await service.create_new_movie(request, database, current_user)
    return movie


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
