from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship

from media_library.db import Base


# class Category(Base):
#     __tablename__ = "category"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String(50))
#     user_id = Column(Integer, ForeignKey('user.id'))
#     users = relationship("User", back_populates='category')
#     media = relationship("Media", back_populates="category")


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
    category_name = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id', ondelete="CASCADE"))
    user = relationship('User', backref='media_user', uselist=False)
    movie = relationship('Movie', backref='media', uselist=False)
    song = relationship('Song', backref='media', uselist=False)
    game = relationship('Game', backref='media', uselist=False)
    __mapper_args__ = {
        'polymorphic_identity': 'media'
    }


class Movie(Base):
    __tablename__ = "movie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    main_actors = Column(Text)
    id_imdb = Column(Integer)
    product_company_name = Column(Text)
    media_id = Column(Integer, ForeignKey('media.id', ondelete="CASCADE"))
    # media = relationship("Media", backref="movie", uselist=False)
    __mapper_args__ = {
        'polymorphic_identity': 'movie'
    }


class Song(Base):
    __tablename__ = "song"

    id = Column(Integer, primary_key=True, autoincrement=True)
    band_name = Column(Text)
    disk_name = Column(Text)
    duration = Column(Float)
    media_id = Column(Integer, ForeignKey('media.id', ondelete="CASCADE"))
    # media = relationship("Media", back_populates="song")
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
    media_id = Column(Integer, ForeignKey('media.id', ondelete="CASCADE"))
    # media = relationship("Media", back_populates="game")
    __mapper_args__ = {
        'polymorphic_identity': 'game'
    }
