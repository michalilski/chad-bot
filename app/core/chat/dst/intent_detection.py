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

    def __init__(self, chatgpt_handler: ChatGPTBridge):
        self.chatgpt_handler = chatgpt_handler

    def fuzzy_intent_matching(self, response: str, intents: List[str]) -> IntentEnum:
        current_intent: str = intents[0]
        max_score: int = 0
        for intent in intents:
            score: int = fuzz.ratio(response, intent)
            if score > max_score:
                current_intent = intent
                max_score = score
        return IntentEnum(current_intent)

    def recognize_intent(self, message: str) -> IntentEnum:
        intents: List[str] = [intent.value for intent in IntentEnum]
        prompt: str = self.id_prompt.format(", ".join(intents), message)
        intent_response: str = self.chatgpt_handler.request(prompt)
        try:
            intent = IntentEnum(intent_response)
        except ValueError:
            logging.warn(f"Unknown intent: {intent_response}. Performing fuzzy matching.")
            intent = self.fuzzy_intent_matching(intent_response, intents)
        return intent
