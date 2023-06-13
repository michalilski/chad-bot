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
        if self["title"].is_empty and self["date"].is_empty:
            return "I need you to provide either a name of the movie or when you want to watch the movie."
        try:
            next_required_slot: SlotMapping = self._get_next_empty_required_slot()
            return nlg.rewrite_outline(
                f"Please tell me those information about the screenings: {next_required_slot.request_template}"
            )
        except NoSlotsToRequest:
            pass
        screenings = self._get_screenings()
        screenings_text = ". ".join(f"Movie {i + 1}: {text}" for i, text in enumerate(screenings))

        criteria = ". ".join(slot.info_template for slot in self._get_all_filled_slots())
        response = nlg.rewrite_outline(
            f"According to the criteria you asked for: {criteria} I found the following screenings:"
            f"{screenings_text}"
            "Which one would you like to book a ticket for?"
        )
        return self._add_suggestions_to_response(nlg, response)

    def _add_suggestions_to_response(self, nlg, response):
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

    def _get_screenings(self):
        # TODO: @michał implement query to to the database.
        return ["Titanic 2 from 2013", "The Bible Rebuild from 1995"]
