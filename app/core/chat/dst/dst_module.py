import dataclasses
import json
import logging
from abc import abstractmethod
from typing import Any, Dict, Optional, Type

from app.core.chat.chatgpt_handler import ChatGPTHandler
from app.core.schemas.state import AbstractState
from app.exceptions import ChatProcessingException


class AbstractDSTModule:
    @abstractmethod
    def parse_state_params(self, text: str, AbstractStateClass: Type[AbstractState]) -> AbstractState:
        """Parse user's utterance to structrized state parameters"""
        pass


class ChatGPTBasedDSTModule(AbstractDSTModule):
    dst_prompt: str = (
        "Extract these exact slot values [{0}]"
        ' in JSON format from a given utterance: "{1}".'
        " Return empty slots as NA."
    )

    def __init__(self, chatgpt_handler: ChatGPTHandler):
        self.chatgpt_handler = chatgpt_handler

    def parse_state_params(self, text: str, AbstractStateClass: Type[AbstractState]) -> AbstractState:
        query_fields: str = self.extract_fields_from_state_class(AbstractStateClass)
        if not query_fields:
            return AbstractStateClass()

        model_query: str = self.dst_prompt.format(query_fields, text)
        model_response: str = self.chatgpt_handler.request(model_query)
        processed_response: Dict[str, Any] = ChatGPTResponseProcessor.process(model_response)
        return self.dict_to_state_params(processed_response, AbstractStateClass)

    def extract_fields_from_state_class(self, AbstractStateClass: Type[AbstractState]) -> str:
        return ", ".join([field.name for field in dataclasses.fields(AbstractStateClass) if field.name != "required"])

    def dict_to_state_params(self, response: Dict[str, Any], AbstractStateClass: Type[AbstractState]) -> AbstractState:
        try:
            state: AbstractState = AbstractStateClass(**response)
        except TypeError as err:
            logging.error(
                f"[DST] Could not parse the response {response} to {AbstractStateClass.__name__} params. -> {err}"
            )
            raise ChatProcessingException
        return state


class ChatGPTResponseProcessor:
    @classmethod
    def process(cls, text: str) -> Dict[str, Any]:
        text = cls.remove_special_characters(text)
        return cls.parse_to_dictionary(text)

    @classmethod
    def remove_special_characters(cls, text: str) -> str:
        return text.replace("\n", "")

    @classmethod
    def parse_to_dictionary(cls, text: str) -> Dict[str, Any]:
        try:
            data: Dict[str, Any] = json.loads(text)
            data = {k: data[k] if data[k] != "NA" else None for k in data}
        except json.JSONDecodeError:
            logging.error(f"[DST] Could not parse text: {text} to dictionary type.")
            raise ChatProcessingException
        return data
