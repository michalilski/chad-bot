import dataclasses
import json
from abc import abstractmethod
from typing import Any, Dict, Type

from app.core.chat.chatgpt_handler import ChatGPTHandler
from app.core.schemas.state import AbstractStateQuery
from app.exceptions import ChatGPTResponseParsingError


class AbstractDSTModule:
    @abstractmethod
    def parse_query_params(self, text: str, StateQueryClass: Type[AbstractStateQuery]) -> AbstractStateQuery:
        """Parse user's utterance to structrized query parameters"""
        pass


class ChatGPTBasedDSTModule(AbstractDSTModule):
    dst_prompt: str = (
        "Extract these exact slot values [{0}]"
        ' in JSON format from a given utterance: "{1}".'
        " Return empty slots as NA."
    )

    def __init__(self, chatgpt_handler: ChatGPTHandler):
        self.chatgpt_handler = chatgpt_handler

    def parse_query_params(self, text: str, StateQueryClass: Type[AbstractStateQuery]) -> AbstractStateQuery:
        model_query: str = self.dst_prompt.format(*[self.extract_fields_from_query_class(StateQueryClass), text])
        model_response: str = self.chatgpt_handler.request(model_query)
        processed_response: Dict[str, Any] = ChatGPTResponseProcessor.process(model_response)
        return self.dict_to_query_params(processed_response, StateQueryClass)

    def extract_fields_from_query_class(self, StateQueryClass: Type[AbstractStateQuery]) -> str:
        return ", ".join([field.name for field in dataclasses.fields(StateQueryClass)])

    def dict_to_query_params(
        self, response: Dict[str, Any], StateQueryClass: Type[AbstractStateQuery]
    ) -> AbstractStateQuery:
        try:
            query: AbstractStateQuery = StateQueryClass(**response)
        except TypeError as err:
            raise ChatGPTResponseParsingError(
                f"Could not parse the response {response} to {StateQueryClass.__name__} params. -> {err}"
            )
        return query


class ChatGPTResponseProcessor:
    @classmethod
    def process(cls, text: str):
        text = cls.remove_special_characters(text)
        data: Dict[str, Any] = cls.parse_to_dictionary(text)
        return cls.multiple_values_to_list(data)

    @classmethod
    def remove_special_characters(cls, text: str) -> str:
        return text.replace("\n", "").replace("NA", "")

    @classmethod
    def parse_to_dictionary(cls, text: str) -> Dict[str, Any]:
        try:
            data: Dict[str, Any] = json.loads(text)
        except json.JSONDecodeError:
            raise ChatGPTResponseParsingError(f"Could not parse text: {text} to dictionary type.")
        return data

    @classmethod
    def multiple_values_to_list(cls, data: Dict[str, Any]):
        for key, values in data.items():
            if type(values) is str:
                data[key] = values.split(", ")
        return data