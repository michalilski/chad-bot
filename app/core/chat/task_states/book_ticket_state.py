from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple

import parsedatetime
from fuzzywuzzy import fuzz
from sqlalchemy import func

from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.task_states.task_state import NoSlotsToRequest, NoSlotsToSuggest, TaskState
from app.core.db.engine import Session
from app.core.db.models import Movie, Show

READY_TO_PURCHASE = bool


@dataclass
class BookTicketState(TaskState):
    suggestions_already_made: bool = False
    matching_title_threshold: int = 50
    query_limit: int = 5

    def __init__(self):
        super().__init__(
            [
                SlotMapping(
                    name="title",
                    description="the title of the movie",
                    _info_template="The movie is called {}",
                    _request_template="Which movie are you interested in?",
                    is_required=False,
                ),
                SlotMapping(
                    name="date",
                    description="the date of the screening of the movie",
                    _info_template="The screening happens on {}",
                    _request_template="What is the date of the screening of the movie?",
                    is_required=False,
                ),
                SlotMapping(
                    name="from_hour",
                    description="beginning hour of requested screenings of the movie",
                    _info_template="The screening are listed from {}",
                    _request_template="From what hour do you want to list the screenings?",
                    is_required=False,
                ),
                SlotMapping(
                    name="to_hour",
                    description="ending hour of requested screenings of the movie",
                    _info_template="The screening are listed until {}",
                    _request_template="Until what hour do you want to list the screenings?",
                    is_required=False,
                ),
                SlotMapping(
                    name="genre",
                    description="genre of the movie",
                    _info_template="The movie is a {}",
                    _request_template="What genre of movies do you want to list?",
                    is_required=False,
                ),
            ]
        )
        self.cal: parsedatetime.Calendar = parsedatetime.Calendar()
        self.movie_titles: Tuple[str, ...] = self.fetch_movie_titles()

    def generate_next_response(self) -> Tuple[str, READY_TO_PURCHASE]:
        if self["title"].is_empty and self["date"].is_empty:
            return (
                "I need you to provide either a name of the movie or when you want to watch the movie.",
                READY_TO_PURCHASE(False),
            )
        try:
            next_required_slot: SlotMapping = self._get_next_empty_required_slot()
            return (
                f"Please tell me those information about the screenings: {next_required_slot.request_template}",
                READY_TO_PURCHASE(False),
            )
        except NoSlotsToRequest:
            pass
        screenings = self._get_screenings()
        return self._generate_outline_for_screenings(screenings)

    def generate_suggestions_outline(self) -> str:
        if self.suggestions_already_made:
            return ""
        self.suggestions_already_made = True

        empty_slots = self._get_all_empty_slots()
        if not empty_slots:
            raise NoSlotsToSuggest()

        suggestions_outline = (
            "You can also specify the following details about the search: "
            f"{', '.join([slot.description for slot in empty_slots])}"
        )
        self.suggestions_already_made = True
        return suggestions_outline

    def _get_screenings(self) -> List[Show]:
        filters: List[bool] = self.prepare_filters()
        with Session() as session:
            results = session.query(Show).join(Movie).filter(*filters).limit(self.query_limit)
        return [show for show in results]

    def _generate_outline_for_screenings(self, screenings: List[Show]) -> Tuple[str, READY_TO_PURCHASE]:
        criteria = ". ".join(slot.info_template for slot in self._get_all_filled_slots())

        if len(screenings) == 0:
            return (
                f"Unfortunately there are no screenings meeting your criteria: {criteria}. Please update your criteria. {self.generate_suggestions_outline()}",
                READY_TO_PURCHASE(False),
            )
        if len(screenings) == 1:
            return (
                f"The screening I found for your criteria is {screenings[0]}. Do you want me to book you a ticket for this movie?",
                READY_TO_PURCHASE(True),
            )
        screenings_text = ". ".join(f"Movie {i + 1}: {text}" for i, text in enumerate(screenings))
        outline = (
            f"According to the criteria you asked for: {criteria} I found the following screenings:"
            f"{screenings_text} "
            "Which one would you like to book a ticket for? "
            f"{self.generate_suggestions_outline()}"
        )
        return outline, READY_TO_PURCHASE(False)

    def prepare_filters(self) -> List[bool]:
        filters: List[bool] = []
        if self["title"].value is not None:
            score_results = [(fuzz.ratio(self["title"].value, m_title), m_title) for m_title in self.movie_titles]
            matching_title = min(score_results, key=lambda x: -x[0])
            if matching_title[0] >= self.matching_title_threshold:
                filters.append(Movie.title == matching_title[1])

        if self["genre"].value is not None:
            filters.append(func.lower(Movie.genre) == self["genre"].value.lower())

        if self["date"].value is not None:
            from_hour: str = "00:00"
            if self["from_hour"].value is not None:
                from_hour = self["from_hour"].value
            parsed_from_time: datetime = self.parse_time(self["date"].value, from_hour)
            filters.append(Show.show_time >= parsed_from_time)

            till_hour: str = "23:59"
            if self["to_hour"].value is not None:
                till_hour = self["to_hour"].value
            parsed_till_time: datetime = self.parse_time(self["date"].value, till_hour)
            filters.append(Show.show_time <= parsed_till_time)

        return filters

    def convert_numeric_time(self, raw_time):
        try:
            x = int(raw_time)
            if x > 24:
                return raw_time[:-2] + ":" + raw_time[-2:]
            return raw_time + ":00"
        except:
            try:
                x = float(raw_time)
                return str(int(x)) + ":" + str("%.2f" % x)[3:]
            except:
                return raw_time

    def fetch_movie_titles(self) -> Tuple[str, ...]:
        with Session() as session:
            movies: Tuple[str, ...] = tuple(res[0] for res in session.query(Movie.title).all())
        return movies

    def parse_time(self, raw_date, raw_time):
        parsed_time = self.convert_numeric_time(raw_time)
        return self.cal.parseDT(f"{raw_date}, {parsed_time}")[0]
