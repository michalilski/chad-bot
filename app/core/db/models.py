from typing import Type

import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base: Type = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    director = sqlalchemy.Column(sqlalchemy.String(length=50))
    year = sqlalchemy.Column(sqlalchemy.Integer)
    genre = sqlalchemy.Column(sqlalchemy.String(length=50))
    summary = sqlalchemy.Column(sqlalchemy.Text)


class Show(Base):
    __tablename__ = "movie_shows"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    movie_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Movie.id))
    show_time = sqlalchemy.Column(sqlalchemy.DateTime)

    movie = relationship("Movie", foreign_keys="Show.movie_id")


class Ticket(Base):
    __tablename__ = "tickets"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    show_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey(Show.id))
    seat_number = sqlalchemy.Column(sqlalchemy.Integer)

    show = relationship("Show", foreign_keys="Ticket.show_id")
