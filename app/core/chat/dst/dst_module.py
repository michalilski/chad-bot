import json
import logging
from typing import Any, Dict

from app.core.chat.chatgpt_bridge import ChatGPTBridge
from app.core.chat.task_states import TaskState
from app.exceptions import ChatProcessingException


class DSTModule:
    dst_prompt: str = (
        "Extract these exact slot values [{0}]"
        ' in JSON format from a given utterance: "{1}".'
        " Return empty slots as NA."
    )

    def __init__(self, chatgpt_bridge: ChatGPTBridge):
        self.chatgpt_bridge = chatgpt_bridge

    def update_state(self, text: str, state: TaskState):
        if not state.slots:
            return
        query_fields: str = ", ".join(state.get_slot_names_with_descriptions())
        print(query_fields)
        model_query: str = self.dst_prompt.format(query_fields, text)
        model_response: str = self.chatgpt_bridge.request(model_query)
        print(model_response)
        slots_values: Dict[str, Any] = ChatGPTResponseProcessor.process(model_response)
        state.update_certain_slots(slots_values)


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
            data = {k: data[k]for k in data if data[k] != "NA"}
        except json.JSONDecodeError:
            logging.error(f"[DST] Could not parse text: {text} to dictionary type.")
            raise ChatProcessingException
        return data
