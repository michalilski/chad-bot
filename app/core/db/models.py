from pydantic import BaseModel
from typing import List
from datetime import datetime


class Movie(BaseModel):
    # TODO fill based on imdb
    imdb_id: str
    title: str 


class MoviePlaytime(BaseModel):
    # TODO fill with necessary fields
    movie: Movie
    dates: List[datetime]