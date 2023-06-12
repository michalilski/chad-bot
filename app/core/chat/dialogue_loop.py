from typing import List, Dict

from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import AbstractIntentDetectionModule
from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states import TaskState, BookTicketState
from app.core.chat.task_states.unknown_state import UnknownState
from app.exceptions import PROCESSING_ERROR_MESSAGE, ChatProcessingException


class DialogueLoop:
    def __init__(
            self,
            dst: DSTModule,
            intent_detector: AbstractIntentDetectionModule,
            nlg: NLG,
    ):
        self.dst: DSTModule = dst
        self.intent_detector: AbstractIntentDetectionModule = intent_detector
        self.nlg: NLG = nlg

        self._current_intent: IntentEnum = IntentEnum.UNKNOWN
        self._current_state: TaskState = UnknownState()
        self._current_message: str = ""
        self._last_response: str = ""
        self._path_iterator = iter(self._main_path_gen(greet_user=False))

    def reset_main_path(self, greet_user: bool = False):
        self._path_iterator = iter(self._main_path_gen(greet_user=greet_user))

    def step(self, message: str) -> str:
        try:
            self._current_message = message
            detected_intent: IntentEnum = self.intent_detector.recognize_intent(message)
            if detected_intent is not IntentEnum.UNKNOWN:
                self._current_intent = detected_intent
            self._update_current_state()
            response = next(self._path_iterator)
            self._last_response = response
            return response
        except ChatProcessingException:
            return PROCESSING_ERROR_MESSAGE

    def _update_current_state(self):
        self.dst.update_state(self._current_message, self._current_state)

    def _main_path_gen(self, greet_user=True):
        if greet_user:
            yield "Hi! How can I help you?"

        while self._current_intent is IntentEnum.UNKNOWN:
            yield "I'm sorry, I did not understand that. I can help you with xxxxx..."

        if self._current_intent is IntentEnum.BOOK_TICKETS:
            yield from self._book_ticket_path_gen()
        elif self._current_intent is IntentEnum.SEE_BOOKING:
            yield from self._see_booking_path_gen()

    def _book_ticket_path_gen(self):
        book_ticket_state: BookTicketState = BookTicketState()
        self._current_state = book_ticket_state
        self._update_current_state()
        while book_ticket_state["title"].is_empty and book_ticket_state["date"].is_empty:
            yield "I need you to provide either a name of the movie or when you want to watch the movie."

        # TODO: obviosly, fix
        while True:
            if self._current_intent is IntentEnum.BOOK_TICKETS:
                yield book_ticket_state.generate_next_response(self.nlg)
            elif self._current_intent is IntentEnum.AFFIRMATIVE:
                yield "YOU ARE A HAPPY OWNER OF THE TICKET!"
            elif self._current_intent is IntentEnum.NEGATIVE:
                yield "No ticket for you then lol!"

    def _see_booking_path_gen(self):
        yield "NOT YET IMPLEMENTED"
