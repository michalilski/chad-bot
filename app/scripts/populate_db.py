import csv
import logging

from app.core.db.engine import db_session
from app.core.db.models import Movie, Show
from app.settings import PROJECT_PATH


def populate_movies(path):
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)
        try:
            for line in reader:
                movie = Movie(
                    imdb_id=line[0],
                    title=line[1],
                    director=line[2],
                    year=line[3],
                    genre=line[4],
                )
                db_session.add(movie)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logging.error(e)


def populate_movie_shows(path):
    with open(path) as file:
        reader = csv.reader(file)
        next(reader)
        try:
            for line in reader:
                show = Show(movie_id=line[0], show_time=line[1])
                db_session.add(show)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logging.error(e)


def populate():
    data_path = PROJECT_PATH / "data" / "csv"
    populate_movies(data_path / "movies.csv")
    populate_movie_shows(data_path / "movie_shows.csv")


if __name__ == "__main__":
    populate()
