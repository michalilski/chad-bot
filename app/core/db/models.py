from typing import Type

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Type = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    imdb_id = sqlalchemy.Column(sqlalchemy.String(length=20), primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(length=100))
    director = sqlalchemy.Column(sqlalchemy.String(length=50))
    year = sqlalchemy.Column(sqlalchemy.Integer)
    genre = sqlalchemy.Column(sqlalchemy.String(length=50))


class Show(Base):
    __tablename__ = "movie_shows"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movie_id = sqlalchemy.Column(sqlalchemy.String(length=20), sqlalchemy.ForeignKey(Movie.imdb_id))
    show_time = sqlalchemy.Column(sqlalchemy.DateTime)

    movie = relationship("Movie", foreign_keys="Show.movie_id", lazy='joined')


class Ticket(Base):
    __tablename__ = "tickets"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    show_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Show.id))
    seat_number = sqlalchemy.Column(sqlalchemy.Integer)
    pin = sqlalchemy.Column(sqlalchemy.Integer)

    show = relationship("Show", foreign_keys="Ticket.show_id", lazy='joined')
