from typing import List

from app.core.chat.dm.dialogue_management import DialogueManagement
from app.core.chat.dst.dst_module import AbstractDSTModule
from app.core.chat.dst.intent_detection import AbstractIntentDetectionModule
from app.core.chat.dst.state_handler import StateHandler
from app.core.chat.nlg.response_generation import AbstractResponseGenerationModule
from app.core.db.engine import db_session
from app.core.enums import IntentEnum
from app.core.schemas.dialogue_action import AbstractDialogueAction
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
        self.dm_module: DialogueManagement = DialogueManagement()

    def answer(self, chat_history: List[str], message: str) -> str:
        try:
            intent: IntentEnum = self.id_module.recognize_intent(message)
            state: AbstractState = self.dst_module.parse_state_params(message, intent_state_mapping[intent])
            current_state, general_state = self.state_handler.update(intent, state)
            dialogue_action: AbstractDialogueAction = self.dm_module.handle_user_request(
                intent, current_state, general_state
            )
            return (
                f"Intent: {intent}"
                f"\n State: {self.state_handler.states[intent]}"
                f"\n General: {self.state_handler.general_state}"
            )
        except ChatProcessingException:
            return PROCESSING_ERROR_MESSAGE
