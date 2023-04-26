from datetime import datetime
from typing import List

from pydantic import BaseModel


class Movie(BaseModel):
    # TODO fill based on imdb
    imdb_id: str
    title: str


class MoviePlaytime(BaseModel):
    # TODO fill with necessary fields
    movie: Movie
    dates: List[datetime]
