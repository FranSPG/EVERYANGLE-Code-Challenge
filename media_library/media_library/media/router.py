from typing import List

from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from media_library import db
from . import schema
from . import service
from . import validator

router = APIRouter(
    tags=['Media'],
    prefix='/medias'
)


@router.post('/category', status_code=status.HTTP_201_CREATED)
async def create_category(request: schema.Category, database: Session = Depends(db.get_db)):
    new_category = await service.create_new_category(request, database)
    return new_category


@router.get('/category', response_model=List[schema.ListCategory])
async def get_all_categories(database: Session = Depends(db.get_db)):
    return await service.get_all_categories(database)


@router.get('/category/{category_id}', response_model=schema.ListCategory)
async def get_category_by_id(category_id: int, database: Session = Depends(db.get_db)):
    return await service.get_category_by_id(category_id, database)


@router.delete('/category/{category_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_category_by_id(category_id: int, database: Session = Depends(db.get_db)):
    return await service.delete_category_by_id(category_id, database)


@router.post('/movies', status_code=status.HTTP_201_CREATED)
async def create_movie(request: schema.Movie, database: Session = Depends(db.get_db)):
    category = await validator.verify_category_exist(request.media.category_id, database)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="You have provided invalid category id.",
        )
    movie = await service.create_new_movie(request, category.id, database)
    return movie


@router.get('/movies', response_model=List[schema.Movie])
async def get_all_movies(database: Session = Depends(db.get_db)):
    return await service.get_all_movies(database)


@router.post('/songs', status_code=status.HTTP_201_CREATED)
async def create_song(request: schema.Song, database: Session = Depends(db.get_db)):
    category = await validator.verify_category_exist(request.media.category_id, database)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="You have provided invalid category id.",
        )

    product = await service.create_new_song(request, category.id, database)
    return product


@router.get('/songs', response_model=List[schema.Song])
async def get_all_songs(database: Session = Depends(db.get_db)):
    return await service.get_all_songs(database)


@router.post('/games', status_code=status.HTTP_201_CREATED)
async def create_game(request: schema.Game, database: Session = Depends(db.get_db)):
    category = await validator.verify_category_exist(request.media.category_id, database)
    if not category:
        raise HTTPException(
            status_code=400,
            detail="You have provided invalid category id.",
        )

    game = await service.create_new_game(request, category.id, database)

    return game


@router.get('/games', response_model=List[schema.Game])
async def get_all_games(database: Session = Depends(db.get_db)):
    return await service.get_all_games(database)
