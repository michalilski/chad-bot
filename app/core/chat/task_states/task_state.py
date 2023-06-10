from abc import abstractmethod
from dataclasses import dataclass, field
from typing import List, Tuple, Dict, Union

from app.core.chat.dialogue_structs.action import Action
from app.core.chat.dialogue_structs.dialogue_act import DialogueActEnum
from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dialogue_structs.slot_mapping import SlotMapping


class TaskState:
    def __init__(self, intent: IntentEnum, slots: List[SlotMapping]):
        self.intent: IntentEnum = intent
        self.slots: List[SlotMapping] = slots

    def reset(self):
        for slot in self.slots:
            slot.set_certain_values(None)

    def update_certain_slots(self, slots_values: Dict[str, Union[str, List[str]]]):
        for slot in self.slots:
            if slot.name not in slots_values:
                continue
            slot.set_certain_values(slots_values[slot.name])

    def update_guessed_slots(self, slots_values: Dict[str, Union[str, List[str]]]):
        for slot in self.slots:
            if slot.name not in slots_values:
                continue
            slot.set_guessed_values(slots_values[slot.name])

    def get_slot_names_with_descriptions(self) -> List[str]:
        return [f"{slot.name} ({slot.description})" for slot in self.slots]

    @abstractmethod
    def generate_next_action(self) -> Action:
        pass

    def _request_next_required_empty_slot(self) -> Action:
        for slot in self.slots:
            if slot.is_required and slot.is_empty:
                return Action(intent=self.intent, act=DialogueActEnum.REQUEST, slot_mappings=[slot])
        raise NoSlotsToRequest()

    def _inform_about_all_filled_slots(self) -> Action:
        filled_slots = [slot for slot in self.slots if not slot.is_empty]
        return Action(intent=self.intent, act=DialogueActEnum.INFORM, slot_mappings=filled_slots)


class NoSlotsToRequest(Exception):
    pass
