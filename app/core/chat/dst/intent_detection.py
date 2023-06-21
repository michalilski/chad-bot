import logging
from abc import abstractmethod
from typing import List

from fuzzywuzzy import fuzz

from app.core.chat.chatgpt_bridge import ChatGPTBridge
from app.core.chat.dialogue_structs.intent import IntentEnum


class AbstractIntentDetectionModule:
    @abstractmethod
    def recognize_intent(self, *args, **kwargs) -> IntentEnum:
        pass


class ChatGPTBasedIntentDetectionModule(AbstractIntentDetectionModule):
    id_prompt: str = "Recognize the intent from list [{0}]" ' for a given utterance: "{1}".'

    def __init__(self):
        self.chatgpt_handler = ChatGPTBridge()

    def recognize_intent(self, message: str) -> IntentEnum:
        intents: str = ", ".join(f"{intent.name} ({intent.value})" for intent in IntentEnum)
        prompt: str = self.id_prompt.format(intents, message)
        intent_response: str = self.chatgpt_handler.request(prompt)
        try:
            intent = IntentEnum(intent_response)
        except ValueError:
            logging.warn(f"Unknown intent: {intent_response}. Performing fuzzy matching.")
            intent = self.fuzzy_intent_matching(intent_response)
        return intent

    def fuzzy_intent_matching(self, response: str) -> IntentEnum:
        current_intent = list(IntentEnum)[0]
        max_score: int = 0
        for intent in IntentEnum:
            score: int = fuzz.ratio(response, intent.name)
            if score > max_score:
                current_intent = intent
                max_score = score
        return current_intent
