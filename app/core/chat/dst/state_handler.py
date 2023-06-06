from collections import defaultdict
from dataclasses import fields
from typing import Any, Dict, Tuple

from app.core.enums import IntentEnum
from app.core.schemas.state import AbstractState, intent_state_mapping


class StateHandler:
    def __init__(self):
        self.states: Dict[IntentEnum, AbstractState] = {
            intent: intent_state_mapping[intent]() for intent in intent_state_mapping
        }
        self.general_state: Dict[str, Any] = defaultdict(lambda _: None)

    def update(self, intent: IntentEnum, state: AbstractState) -> Tuple[AbstractState, Dict[str, Any]]:
        previous_state: AbstractState = self.states[intent]
        for field in fields(state):
            if field.name == "required":
                continue

            previous_value: Any = previous_state.__getattribute__(field.name)
            current_value: Any = state.__getattribute__(field.name)

            if not self.should_update(previous_value, current_value):
                continue

            self.states[intent].__setattr__(field.name, current_value)
            self.general_state[field.name] = current_value
        return self.states[intent], self.general_state

    def should_update(self, previous: Any, current: Any) -> bool:
        return previous is None or current is not None
