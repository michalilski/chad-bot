from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.task_states.task_state import NoSlotsToRequest, NoSlotsToSuggest, TaskState
from app.core.db.db_bridge import DatabaseBridge
from app.core.db.models import Show


@dataclass
class ReadyToPurchase:
    screening: Optional[Show]

    def __bool__(self):
        return self.screening is not None

    @classmethod
    def not_ready(cls) -> ReadyToPurchase:
        return ReadyToPurchase(None)


@dataclass
class BookTicketState(TaskState):
    matching_title_threshold: int = 50
    query_limit: int = 5

    def __init__(self):
        super().__init__(
            [
                SlotMapping(
                    name="movie_title",
                    description="title of the movie that the user want to buy ticket for",
                    _info_template="The movie is called {}",
                    _request_template="Which movie are you interested in?",
                    is_required=False,
                ),
                SlotMapping(
                    name="movie_date",
                    description="the date of the screening of the movie that the user want to buy ticket for",
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
                    name="movie_genre",
                    description="genre of the movie that the user want to buy ticket for",
                    _info_template="The movie is a {}",
                    _request_template="What genre of movies do you want to list?",
                    is_required=False,
                ),
            ]
        )
        self.suggestions_already_made: bool = False

    def generate_next_response(self) -> Tuple[str, ReadyToPurchase]:
        if self["movie_title"].is_empty and self["movie_date"].is_empty:
            return (
                "I need you to provide either a name of the movie or when you want to watch the movie.",
                ReadyToPurchase.not_ready(),
            )
        try:
            next_required_slot: SlotMapping = self._get_next_empty_required_slot()
            return (
                f"Please tell me those information about the screenings: {next_required_slot.request_template}",
                ReadyToPurchase.not_ready(),
            )
        except NoSlotsToRequest:
            pass
        screenings = self._get_screenings()
        return self._generate_outline_for_screenings(screenings)

    def generate_suggestions_outline(self) -> str:
        suggestions_outline: str = (
            "Currently I am booking a ticket for you."
            f"Here are the details you already provided {[{slot.description: slot.value} for slot in self._get_all_filled_slots()]}."
            f"Here are the details you can also provide {[slot.description for slot in self._get_all_empty_slots()]}."
        )
        return suggestions_outline

    def generate_empty_slots_suggestions_outline(self) -> str:
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
        return DatabaseBridge.get_screenings(
            title=self["movie_title"].value,
            genre=self["movie_genre"].value,
            date=self["movie_date"].value,
            from_hour=self["from_hour"].value,
            to_hour=self["to_hour"].value,
            matching_title_threshold=self.matching_title_threshold,
            query_limit=self.query_limit,
        )

    def _generate_outline_for_screenings(self, screenings: List[Show]) -> Tuple[str, ReadyToPurchase]:
        criteria = ". ".join(slot.info_template for slot in self._get_all_filled_slots())

        if len(screenings) == 0:
            return (
                f"Unfortunately there are no screenings meeting your criteria: {criteria}. Please update your criteria. {self.generate_empty_slots_suggestions_outline()}",
                ReadyToPurchase.not_ready(),
            )
        if len(screenings) == 1:
            return (
                f"The screening I found for your criteria is {screenings[0]}. Do you want me to book you a ticket for this movie?",
                ReadyToPurchase(screenings[0]),
            )
        screenings_text = ", ".join(f"{i + 1}: {text}" for i, text in enumerate(screenings))
        outline = (
            f"According to the criteria you asked for: {criteria} I found the following screenings:"
            f"{screenings_text} "
            "Which one would you like to book a ticket for? "
            f"{self.generate_suggestions_outline()}"
        )
        return outline, ReadyToPurchase.not_ready()
