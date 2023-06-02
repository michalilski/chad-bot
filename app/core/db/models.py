from datetime import datetime
from typing import List


class Movie:
    # TODO fill based on imdb
    imdb_id: str
    title: str


class MoviePlaytime:
    # TODO fill with necessary fields
    movie: Movie
    dates: List[datetime]
