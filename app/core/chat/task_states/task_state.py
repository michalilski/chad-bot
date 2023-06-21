from abc import abstractmethod
from typing import Dict, List, Union

from app.core.chat.dialogue_structs.intent import IntentEnum
from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.nlg.nlg import NLG


class TaskState:
    def __init__(self, slots: List[SlotMapping]):
        self.slots: List[SlotMapping] = slots

    def __getitem__(self, slot_name: str) -> SlotMapping:
        for slot in self.slots:
            if slot.name == slot_name:
                return slot
        raise ValueError(f"No slot named {slot_name}")

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
        return [f'"{slot.name}" ({slot.description})' for slot in self.slots]

    @abstractmethod
    def generate_suggestions_outline(self) -> str:
        pass

    def _get_next_empty_required_slot(self) -> SlotMapping:
        for slot in self.slots:
            if slot.is_required and slot.is_empty:
                return slot
        raise NoSlotsToRequest()

    def _get_all_filled_slots(self) -> List[SlotMapping]:
        return [slot for slot in self.slots if not slot.is_empty]

    def _get_all_empty_slots(self) -> List[SlotMapping]:
        return [slot for slot in self.slots if slot.is_empty]


class NoSlotsToRequest(Exception):
    pass


class NoSlotsToSuggest(Exception):
    pass
