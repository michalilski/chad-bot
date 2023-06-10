from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class SlotMapping:
    name: str
    description: str
    is_required: bool = False
    _is_guessed: bool = False
    _values: Optional[List[str]] = None

    @property
    def is_empty(self) -> bool:
        return self.values is None

    def is_guessed(self) -> bool:
        return self._is_guessed

    @property
    def values(self) -> Optional[List[str]]:
        return self._values

    @values.setter
    def values(self, value: Optional[List[str]]):
        raise RuntimeError("Please set values by a method, not a setter.")

    def set_certain_values(self, values: Optional[Union[str, List[str]]]):
        if isinstance(values, str):
            values = [values]
        self._values = values
        self._is_guessed = False

    def set_guessed_values(self, values: Optional[Union[str, List[str]]]):
        if isinstance(values, str):
            values = [values]
        self._values = values
        self._is_guessed = True

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if isinstance(other, str):
            return self.name == other
        if isinstance(other, SlotMapping):
            return self is other
        return False
