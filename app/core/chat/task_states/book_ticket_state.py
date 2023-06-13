from dataclasses import dataclass
from typing import List, Tuple

from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states.task_state import TaskState, NoSlotsToRequest, NoSlotsToSuggest

READY_TO_PURCHASE = bool


@dataclass
class BookTicketState(TaskState):
    def __init__(self):
        super().__init__(
            [
                SlotMapping(
                    name="title",
                    description="the title of the movie",
                    _info_template="The movie is called {}",
                    _request_template="Which movie are you interested in?",
                    is_required=False
                ),
                SlotMapping(
                    name="date",
                    description="the date of the screening of the movie",
                    _info_template="The screening happens on {}",
                    _request_template="What is the date of the screening of the movie?",
                    is_required=False
                ),
                SlotMapping(
                    name="from_hour",
                    description="beginning hour of requested screenings of the movie",
                    _info_template="The screening are listed from {}",
                    _request_template="From what hour do you want to list the screenings?",
                    is_required=False
                ),
                SlotMapping(
                    name="to_hour",
                    description="ending hour of requested screenings of the movie",
                    _info_template="The screening are listed until {}",
                    _request_template="Until what hour do you want to list the screenings?",
                    is_required=False
                ),
                SlotMapping(
                    name="date",
                    description="the date of the screening of the movie",
                    _info_template="The screening happens on {}",
                    _request_template="What is the date of the screening of the movie?",
                    is_required=False
                ),
                SlotMapping(
                    name="genre",
                    description="genre of the movie",
                    _info_template="The movie is a {}",
                    _request_template="What genre of movies do you want to list?",
                    is_required=False
                ),
            ]
        )
        self.suggestions_already_made = False

    def generate_next_response(self, nlg: NLG) -> Tuple[str, READY_TO_PURCHASE]:
        if self["title"].is_empty and self["date"].is_empty:
            return nlg.rewrite_outline("I need you to provide either a name of the movie or when you want to watch the movie."), READY_TO_PURCHASE(False)
        try:
            next_required_slot: SlotMapping = self._get_next_empty_required_slot()
            return nlg.rewrite_outline(
                f"Please tell me those information about the screenings: {next_required_slot.request_template}"
            ), READY_TO_PURCHASE(False)
        except NoSlotsToRequest:
            pass
        screenings = self._get_screenings()
        outline, ready_to_purchase = self._generate_outline_for_screenings(screenings)
        response = nlg.rewrite_outline(outline)
        return response, ready_to_purchase

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

    def _get_screenings(self) -> List[str]:
        # TODO: @michał implement query to to the database.
        return ["Titanic 2 from 2013"]
        return []
        return ["Titanic 2 from 2013", "The Bible Rebuild from 1995"]

    def _generate_outline_for_screenings(self, screenings: List[str]) -> Tuple[str, READY_TO_PURCHASE]:
        criteria = ". ".join(slot.info_template for slot in self._get_all_filled_slots())

        if len(screenings) == 0:
            return f"Unfortunately there are no screenings meeting your criteria: {criteria}. Please update your criteria. {self.generate_suggestions_outline()}", READY_TO_PURCHASE(
                False
            )
        if len(screenings) == 1:
            return f"The screening I found for your criteria is {screenings[0]}. Do you want me to book you a ticket for this movie?", READY_TO_PURCHASE(True)
        screenings_text = ". ".join(f"Movie {i + 1}: {text}" for i, text in enumerate(screenings))
        outline = (
            f"According to the criteria you asked for: {criteria} I found the following screenings:"
            f"{screenings_text} "
            "Which one would you like to book a ticket for? "
            f"{self.generate_suggestions_outline()}"
        )
        return outline, READY_TO_PURCHASE(False)
