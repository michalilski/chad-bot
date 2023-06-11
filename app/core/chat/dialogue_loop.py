from typing import List, Dict

from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dst.dst_module import DSTModule
from app.core.chat.dst.intent_detection import AbstractIntentDetectionModule
from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states import TaskState, ListMoviesState
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

        self.last_intent: IntentEnum = IntentEnum.UNKNOWN
        self.states: Dict[IntentEnum, TaskState] = {
            IntentEnum.LIST_MOVIES: ListMoviesState(),
        }

    def answer(self, chat_history: List[str], message: str) -> str:
        try:
            current_intent: IntentEnum = self.intent_detector.recognize_intent(message)
            if current_intent is IntentEnum.GIVE_SUGGESTIONS:
                return self.states[self.last_intent].generate_suggestions(self.nlg)
            if current_intent is IntentEnum.UNKNOWN:
                current_intent = self.last_intent
            # NOTE: reset the state if intent changed?
            self.last_intent = current_intent
            current_state: TaskState = self.states[current_intent]
            self.dst.update_state(message, current_state)

            return current_state.generate_next_response(self.nlg)
        except ChatProcessingException:
            return PROCESSING_ERROR_MESSAGE
