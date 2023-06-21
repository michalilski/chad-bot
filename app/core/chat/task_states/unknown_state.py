from dataclasses import dataclass

from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states.task_state import TaskState


@dataclass
class UnknownState(TaskState):
    def __init__(self):
        super().__init__([])

    def generate_next_response(self, nlg: NLG) -> str:
        return "This is a bug. Should not be called."

    def generate_suggestions_outline(self) -> str:
        return (
            "Hello I am a cinema chatbot service called TODD. I can help you with"
            " booking a ticket for a movie you want and you will get a reservation PIN,"
            " if you have a PIN number I can tell you the details or cancel the reservation."
        )
