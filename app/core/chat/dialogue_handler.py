from typing import List

from app.core.chat.dst_module import AbstractDSTModule
from app.core.chat.intent_detection import AbstractIntentDetectionModule
from app.core.chat.response_generation import AbstractResponseGenerationModule
from app.core.chat.state_handler import StateHandler
from app.core.enums import IntentEnum
from app.core.schemas.state import AbstractState, intent_state_mapping
from app.exceptions import PROCESSING_ERROR_MESSAGE, ChatProcessingException


class DialogueHandler:
    def __init__(
        self,
        dst_module: AbstractDSTModule,
        id_module: AbstractIntentDetectionModule,
        nlg_module: AbstractResponseGenerationModule,
    ):
        self.dst_module: AbstractDSTModule = dst_module
        self.id_module: AbstractIntentDetectionModule = id_module
        self.nlg_module: AbstractResponseGenerationModule = nlg_module
        self.state_handler: StateHandler = StateHandler()

    def answer(self, chat_history: List[str], message: str) -> str:
        try:
            intent: IntentEnum = self.id_module.recognize_intent(message)
            state: AbstractState = self.dst_module.parse_state_params(message, intent_state_mapping[intent])
            self.state_handler.update(intent, state)
            return (
                f"Intent: {intent}"
                f"\n State: {self.state_handler.states[intent]}"
                f"\n General: {self.state_handler.general_state}"
            )
        except ChatProcessingException:
            return PROCESSING_ERROR_MESSAGE
