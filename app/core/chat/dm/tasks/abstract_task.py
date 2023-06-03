from abc import abstractmethod
from typing import Any, Dict

from app.core.enums import IntentEnum
from app.core.schemas.dialogue_action import AbstractDialogueAction
from app.core.schemas.state import AbstractState


class AbstractTask:
    @abstractmethod
    def execute(
        self, intent: IntentEnum, state: AbstractState, general_state: Dict[str, Any]
    ) -> AbstractDialogueAction:
        pass
