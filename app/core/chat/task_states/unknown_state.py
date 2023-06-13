from dataclasses import dataclass

from app.core.chat.nlg.nlg import NLG
from app.core.chat.task_states.task_state import TaskState


@dataclass
class UnknownState(TaskState):
    def __init__(self):
        super().__init__([])

    def generate_next_response(self, nlg: NLG) -> str:
        return "I'm sorry I dont understand. Im in unknown state. Patch me :x"

    def generate_suggestions_outline(self) -> str:
        return "Tell me dyour deepest desires. Maybe that will help. Im unknown state."
