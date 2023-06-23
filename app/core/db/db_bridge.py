import logging
import random
from datetime import datetime
from typing import List, Optional, Tuple

from fuzzywuzzy import fuzz
from sqlalchemy import func

from app.core.db.engine import Session
from app.core.db.models import Movie, Show, Ticket
from app.core.db.utils import parse_time


class DatabaseBridge:
    @staticmethod
    def fetch_movie_titles() -> Tuple[str, ...]:
        with Session() as session:
            movies: Tuple[str, ...] = tuple(res[0] for res in session.query(Movie.title).all())
        return movies

    @staticmethod
    def get_screenings(
            title: Optional[str] = None,
            genre: Optional[str] = None,
            date: Optional[str] = None,
            from_hour: Optional[str] = None,
            to_hour: Optional[str] = None,
            matching_title_threshold: int = 50,
            query_limit: int = 5,
    ) -> List[Show]:
        filters: List[bool] = []
        if title is not None:
            score_results = [(fuzz.ratio(title, m_title), m_title) for m_title in DatabaseBridge.fetch_movie_titles()]
            matching_title = min(score_results, key=lambda x: -x[0])
            if matching_title[0] >= matching_title_threshold:
                filters.append(Movie.title == matching_title[1])
            else:
                return []

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

    @staticmethod
    def book_ticket(show: Show, fix_pin: Optional[int] = None) -> Ticket:
        ticket = Ticket(show_id=show.id, seat_number=13, pin=fix_pin or random.randint(1000, 9999))
        with Session() as db_session:
            db_session.add(ticket)
            db_session.commit()
        return ticket

    @staticmethod
    def get_bookings_for_pin(pin: str) -> List[Ticket]:
        try:
            parsed_pin: int = int(pin)
        except ValueError:
            logging.warning(f"Cannot parse pin {pin}")
            return []
        with Session() as session:
            results = session.query(Ticket).filter(Ticket.pin == parsed_pin).limit(10)
        return [ticket for ticket in results]

    @staticmethod
    def get_all_bookings() -> List[Ticket]:
        with Session() as session:
            results = session.query(Ticket).limit(10)
        return [ticket for ticket in results]

    @staticmethod
    def cancel_ticket(pin: str) -> Optional[Ticket]:
        tickets: List[Ticket] = DatabaseBridge.get_bookings_for_pin(pin)
        if not tickets:
            return None
        ticket = tickets[-1]
        with Session() as db_session:
            ticket = db_session.merge(ticket)
            db_session.delete(ticket)
            db_session.commit()
        return ticket

    @staticmethod
    def setup_example_bookings():
        with Session() as db_session:
            for ticket in db_session.query(Ticket):
                db_session.delete(ticket)

            DatabaseBridge.book_ticket(
                DatabaseBridge.get_screenings(title="The Evil Within")[0]
            )
            DatabaseBridge.book_ticket(
                DatabaseBridge.get_screenings(date="tomorrow")[0]
            )
            DatabaseBridge.book_ticket(
                DatabaseBridge.get_screenings(date="tomorrow")[1]
            )
            DatabaseBridge.book_ticket(
                DatabaseBridge.get_screenings(date="July 6th")[2]
            )

            db_session.commit()
