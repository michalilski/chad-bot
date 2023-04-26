from typing import List

from app.core.chat.dst_module import AbstractDSTModule
from app.core.chat.intent_detection import AbstractIntentDetectionModule
from app.core.chat.response_generation import AbstractResponseGenerationModule


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

    def answer(self, chat_history: List[str], message: str) -> str:
        # TODO implement submodules and combine here
        return f"Empty template answer {len(chat_history)}"
