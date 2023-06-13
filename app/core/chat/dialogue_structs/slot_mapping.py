from dataclasses import dataclass
from typing import List, Optional, Union


@dataclass
class SlotMapping:
    name: str
    description: str
    _info_template: str
    _request_template: str
    is_required: bool = False
    _is_guessed: bool = False
    _values: Optional[List[str]] = None

    @property
    def is_empty(self) -> bool:
        return self.values is None

    @property
    def is_filled(self) -> bool:
        return not self.is_empty

    def is_guessed(self) -> bool:
        return self._is_guessed

    @property
    def values(self) -> Optional[List[str]]:
        return self._values

    @property
    def value(self) -> Optional[str]:
        try:
            return self._values[0]  # type: ignore
        except TypeError:
            return None

    @values.setter  # type: ignore
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

    @property
    def info_template(self):
        return self._info_template.format(*self._values)

    @property
    def request_template(self):
        return self._request_template
