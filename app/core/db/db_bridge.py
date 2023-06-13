from datetime import datetime
from typing import List, Optional, Tuple

from fuzzywuzzy import fuzz
from sqlalchemy import func

from app.core.db.engine import Session
from app.core.db.models import Movie, Show
from app.core.db.utils import parse_time


class DatabaseBridge:
    def fetch_movie_titles(self) -> Tuple[str, ...]:
        with Session() as session:
            movies: Tuple[str, ...] = tuple(res[0] for res in session.query(Movie.title).all())
        return movies

    def get_screenings(
        self,
        title: Optional[str],
        genre: Optional[str],
        date: Optional[str],
        from_hour: Optional[str],
        to_hour: Optional[str],
        possible_movie_titles: Tuple[str, ...],
        matching_title_threshold: int = 50,
        query_limit: int = 5,
    ) -> List[Show]:
        filters: List[bool] = []
        if title is not None:
            score_results = [(fuzz.ratio(title, m_title), m_title) for m_title in possible_movie_titles]
            matching_title = min(score_results, key=lambda x: -x[0])
            if matching_title[0] >= matching_title_threshold:
                filters.append(Movie.title == matching_title[1])

        if genre is not None:
            filters.append(func.lower(Movie.genre) == genre.lower())

        if date is not None:
            from_hour = from_hour or "00:00"
            parsed_from_time: datetime = parse_time(date, from_hour)
            filters.append(Show.show_time >= parsed_from_time)

            to_hour = to_hour or "23:59"
            parsed_till_time: datetime = parse_time(date, to_hour)
            filters.append(Show.show_time <= parsed_till_time)

        with Session() as session:
            results = session.query(Show).join(Movie).filter(*filters).limit(query_limit)

        return [show for show in results]
