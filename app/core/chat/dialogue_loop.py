import logging

from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dst.dst_module import STATE_CHANGED, DSTModule
from app.core.chat.dst.intent_detection import AbstractIntentDetectionModule
from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states import BookTicketState, TaskState
from app.core.chat.task_states.book_ticket_state import ReadyToPurchase
from app.core.chat.task_states.manage_booking_state import ManageBookingState
from app.core.chat.task_states.unknown_state import UnknownState
from app.core.db.db_bridge import DatabaseBridge
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
        self._last_system_response: str = ""
        self._last_system_response_outline: str = ""
        self._path_iterator = iter(self._main_path_gen(greet_user=False))

    def reset_main_path(self, greet_user: bool = False):
        self._current_intent = IntentEnum.UNKNOWN
        self._path_iterator = iter(self._main_path_gen(greet_user=greet_user))

    def step(self, message: str) -> str:
        try:
            self._current_message = message
            detected_intent: IntentEnum = self.intent_detector.recognize_intent(message)
            if detected_intent is not IntentEnum.UNKNOWN:
                self._current_intent = detected_intent
            # if detected_intent is IntentEnum.CANCEL_PROCEDURE:
            #     self.reset_main_path()
            #     return "I see you want to do something different... What do you want to do right now then?"
            self._update_current_state()
            outline = next(self._path_iterator)
            response = self.nlg.rewrite_outline(outline, user_message=self._current_message)
            self._last_system_response_outline = outline
            self._last_system_response = response
            return response
        except ChatProcessingException:
            return PROCESSING_ERROR_MESSAGE
        except StopIteration:
            self.reset_main_path()
            return self.step(message)

    def _update_current_state(self) -> STATE_CHANGED:
        return self.dst.update_state(
            system_utterance=self._last_system_response_outline,
            user_utterance=self._current_message,
            state=self._current_state,
        )

    def _main_path_gen(self, greet_user=True):
        if greet_user:
            yield "Hi! How can I help you?"

        while self._current_intent is IntentEnum.UNKNOWN:
            yield "Is there anything I can help you with?"

        if self._current_intent is IntentEnum.BOOK_TICKETS:
            yield from self._book_ticket_path_gen()
        elif self._current_intent is IntentEnum.SEE_BOOKING:
            yield from self._see_booking_path_gen()

    def _book_ticket_path_gen(self):
        book_ticket_state: BookTicketState = BookTicketState()
        self._current_state = book_ticket_state
        self._update_current_state()

        ready_to_purchase = ReadyToPurchase.not_ready()
        while True:
            while not ready_to_purchase:
                response, ready_to_purchase = book_ticket_state.generate_next_response()
                yield response
            # System is ready to make a purchase
            if self._current_intent is IntentEnum.AFFIRMATIVE:
                screening = ready_to_purchase.screening
                ticket = DatabaseBridge.book_ticket(screening)
                yield f"I booked you the ticket for {screening}. The pin for your reservation is {ticket.pin}. Please remember it!"
                return
            else:
                response, ready_to_purchase = book_ticket_state.generate_next_response()
                yield "Okay, I won't buy this ticket unless you say so. " + response

    def _see_booking_path_gen(self):
        manage_booking_state: ManageBookingState = ManageBookingState()
        self._current_state = manage_booking_state
        self._update_current_state()

        while True:
            # TODO: exit condition
            response = manage_booking_state.generate_next_response()
            yield response
