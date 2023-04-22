import dataclasses
import json
from abc import abstractmethod
from typing import Any, Dict, Type

from app.core.chat.chatgpt_handler import ChatGPTHandler
from app.core.chat.exceptions import UtteranceHandlerException
from app.core.schemas.query import AbstractQueryParameters


class AbstractDSTModule:
    @abstractmethod
    def parse_query_params(self, text: str, QueryParametersClass: Type[AbstractQueryParameters]) -> AbstractQueryParameters:
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

    def parse_query_params(self, text: str, QueryParametersClass: Type[AbstractQueryParameters]) -> AbstractQueryParameters:
        model_query: str = self.dst_prompt.format(*[self.extract_fields_from_query_class(QueryParametersClass), text])
        model_response: str = self.chatgpt_handler.request(model_query)
        processed_response: Dict[str, Any] = ChatGPTResponseProcessor.process(model_response)
        return self.dict_to_query_params(processed_response, QueryParametersClass)

    def extract_fields_from_query_class(self, QueryParametersClass: Type[AbstractQueryParameters]) -> str:
        return ", ".join([field.name for field in dataclasses.fields(QueryParametersClass)])

    def dict_to_query_params(
        self, response: Dict[str, Any], QueryParametersClass: Type[AbstractQueryParameters]
    ) -> AbstractQueryParameters:
        try:
            query: AbstractQueryParameters = QueryParametersClass(**response)
        except TypeError as err:
            raise UtteranceHandlerException(
                f"Could not parse the response {response} to {QueryParametersClass.__name__} params. -> {err}"
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
            raise UtteranceHandlerException(f"Could not parse text: {text} to dictionary type.")
        return data

    @classmethod
    def multiple_values_to_list(cls, data: Dict[str, Any]):
        for key, values in data.items():
            if type(values) is str:
                data[key] = values.split(", ")
        return data
