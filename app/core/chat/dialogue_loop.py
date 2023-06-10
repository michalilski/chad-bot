from typing import List, Dict

from app.core.chat.dialogue_structs.action import Action, OutlineElement
from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import AbstractIntentDetectionModule
from app.core.chat.nlg.response_generation import AbstractResponseGenerationModule
from app.core.chat.task_states.states import TaskState, ListMoviesState
from app.exceptions import PROCESSING_ERROR_MESSAGE, ChatProcessingException


class DialogueLoop:
    def __init__(
        self,
        dst: DSTModule,
        intent_detector: AbstractIntentDetectionModule,
        nlg: AbstractResponseGenerationModule,
    ):
        self.dst: DSTModule = dst
        self.intent_detector: AbstractIntentDetectionModule = intent_detector
        self.nlg: AbstractResponseGenerationModule = nlg

        self.last_intent: IntentEnum = IntentEnum.UNKNOWN
        self.states: Dict[IntentEnum, TaskState] = {
            IntentEnum.LIST_MOVIES: ListMoviesState(),
            # IntentEnum.BUY_TICKET: BuyTicketState,
            # IntentEnum.MOVIE_SUMMARY: MovieSummaryState,
            # IntentEnum.CANCEL_INTENT: CancelIntentState,
            # IntentEnum.CANCEL_RESERVATION: CancelReservationState,
            # IntentEnum.UNKNOWN: UnknownIntentState,
        }

    def answer(self, chat_history: List[str], message: str) -> str:
        try:
            current_intent: IntentEnum = self.intent_detector.recognize_intent(message)
            if current_intent is IntentEnum.UNKNOWN:
                current_intent = self.last_intent
            # NOTE: reset the state if intent changed?
            self.last_intent = current_intent
            current_state: TaskState = self.states[current_intent]
            self.dst.update_state(message, current_state)

            outline_elements: List[OutlineElement] = current_state.generate_next_actions()
            outline = " ".join([action.generate_outline() for action in outline_elements])

            return outline
        except ChatProcessingException:
            return PROCESSING_ERROR_MESSAGE
