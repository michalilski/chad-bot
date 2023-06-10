from dataclasses import dataclass
from typing import List

from app.core.chat.dialogue_structs.dialogue_act import DialogueActEnum
from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dialogue_structs.slot_mapping import SlotMapping


@dataclass
class Action:
    intent: IntentEnum
    act: DialogueActEnum
    slot_mappings: List[SlotMapping]

    def generate_outline(self) -> str:
        return f"{self.intent}, {self.act}({[(slot.name, slot.values) for slot in self.slot_mappings]})"
