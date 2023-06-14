import json
import logging
from typing import Any, Dict

from app.core.chat.chatgpt_bridge import ChatGPTBridge
from app.core.chat.task_states import TaskState
from app.exceptions import ChatProcessingException

STATE_CHANGED = bool


class DSTModule:
    dst_prompt: str = (
        'Given system utterance "{1}" and a user response: "{2}"'
        " extract these exact user slot values from [{0}]."
        ' Return results as a JSON. Fill empty or don\'t care slots as "NA".'
    )

    def __init__(self):
        self.chatgpt_bridge = ChatGPTBridge()

    def update_state(self, system_utterance: str, user_utterance: str, state: TaskState) -> STATE_CHANGED:
        if not state.slots:
            return STATE_CHANGED(False)
        query_fields: str = ", ".join(state.get_slot_names_with_descriptions())
        model_query: str = self.dst_prompt.format(query_fields, user_utterance, system_utterance)
        model_response: str = self.chatgpt_bridge.request(model_query)
        slots_values: Dict[str, Any] = ChatGPTResponseProcessor.process(model_response)
        state.update_certain_slots(slots_values)
        # TODO: Implement this check. First make sure that it is used somewhere.
        return STATE_CHANGED(True)


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
            text = text[text.index("{"):text.index("}")+1]
            data: Dict[str, Any] = json.loads(text)
            data = {k: data[k] for k in data if data[k] != "NA"}
            logging.warn(data)
        except json.JSONDecodeError:
            logging.error(f"[DST] Could not parse text: {text} to dictionary type.")
            raise
        return data
