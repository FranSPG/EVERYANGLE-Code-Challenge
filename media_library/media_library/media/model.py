from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from media_library.db import Base


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    media = relationship("Media", back_populates="category")


class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    created_date = Column(DateTime)
    added_date = Column(DateTime, default=datetime.now)
    description = Column(Text)
    genre = Column(Text)
    estimated_budget = Column(Float)
    adult = Column(Boolean)
    original_language = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship("Category", back_populates="media")
    movie = relationship('Movie', back_populates='media')
    song = relationship('Song', back_populates='media')
    game = relationship('Game', back_populates='media')
    __mapper_args__ = {
        'polymorphic_identity': 'media'
    }


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    main_actors = Column(Text)
    id_imdb = Column(Integer)
    product_company_name = Column(Text)
    media_id = Column(Integer, ForeignKey('media.id'))
    media = relationship("Media", back_populates="movie")
    __mapper_args__ = {
        'polymorphic_identity': 'movie'
    }


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, autoincrement=True)
    band_name = Column(Text)
    disk_name = Column(Text)
    duration = Column(Float)
    media_id = Column(Integer, ForeignKey('media.id'))
    media = relationship("Media", back_populates="song")
    __mapper_args__ = {
        'polymorphic_identity': 'song'
    }


class Game(Base):
    __tablename__ = "game"

    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(Text)
    publisher = Column(Text)
    is_free = Column(Boolean)
    game_category = Column(Text)
    est_playable_minutes = Column(Float)
    media_id = Column(Integer, ForeignKey('media.id'))
    media = relationship("Media", back_populates="game")
    __mapper_args__ = {
        'polymorphic_identity': 'game'
    }
