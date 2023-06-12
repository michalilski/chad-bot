from dataclasses import dataclass
from typing import List

from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states.task_state import TaskState, NoSlotsToRequest, NoSlotsToSuggest


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

    def generate_next_response(self, nlg: NLG) -> str:
        try:
            next_required_slot: SlotMapping = self._get_next_empty_required_slot()
            outline = f"Please tell me those information about the screenings: {next_required_slot.request_template}"
            return nlg.rewrite_outline(outline)
        except NoSlotsToRequest:
            pass
        filled_slots: List[SlotMapping] = self._get_all_filled_slots()
        criteria = ". ".join(slot.info_template for slot in filled_slots)
        screenings = "Movie 1: Titanic 2 from 2013, Movie 2: The Bible Rebuild from 1995."

        outline = (
            f"According to the criteria you asked for: {criteria} I found the following screenings:"
            f"{screenings}"
            "Which one would you like to book a ticket for?"
        )
        response = nlg.rewrite_outline(outline)
        if not self.suggestions_already_made:
            suggestions = self.generate_suggestions(nlg)
            response = f"{response} {suggestions}"
            self.suggestions_already_made = True
        return response

    def generate_suggestions(self, nlg: NLG) -> str:
        empty_slots = self._get_all_empty_slots()
        if not empty_slots:
            raise NoSlotsToSuggest()

        suggestions_outline = (
            "You can also specify the following details about the search: "
            f"{', '.join([slot.description for slot in empty_slots])}"
        )
        suggestions = nlg.rewrite_outline(suggestions_outline)
        return suggestions
