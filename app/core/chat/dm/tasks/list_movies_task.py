from typing import Any, Dict

from app.core.chat.dm.tasks.abstract_task import AbstractTask
from app.core.enums import IntentEnum
from app.core.schemas.dialogue_action import AbstractDialogueAction
from app.core.schemas.state import AbstractState


class ListMoviesTask(AbstractTask):
    def execute(
        self, intent: IntentEnum, state: AbstractState, general_state: Dict[str, Any]
    ) -> AbstractDialogueAction:
        # TODO
        raise NotImplementedError
