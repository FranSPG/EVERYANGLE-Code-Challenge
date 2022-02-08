from __future__ import annotations

import datetime

from typing import Optional

from pydantic import BaseModel, constr


class ListCategory(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class MediaBase(BaseModel):
    name: str
    created_date: datetime.date
    added_date: datetime.date
    description: str
    genre: str
    estimated_budget: float
    adult: bool
    original_language: str
    category_name: str

    class Config:
        orm_mode = True


class Movie(BaseModel):
    media: MediaBase
    main_actors: str
    id_imdb: int
    product_company_name: str

    class Config:
        orm_mode = True


class Song(BaseModel):
    media: MediaBase
    band_name: str
    disk_name: str
    duration: float

    class Config:
        orm_mode = True


class Game(BaseModel):
    media: MediaBase
    platform: str
    publisher: str
    is_free: bool
    game_category: str
    est_playable_minutes: float

    class Config:
        orm_mode = True
