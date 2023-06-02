from typing import Any, Dict

from app.core.enums import IntentEnum
from app.core.schemas.dialogue_action import AbstractDialogueAction
from app.core.schemas.state import AbstractState


class DialogueManagement:
    def handle_user_request(
        self, intent: IntentEnum, state: AbstractState, general_state: Dict[str, Any]
    ) -> AbstractDialogueAction:
        # TODO
        return AbstractDialogueAction()
