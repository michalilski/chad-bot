import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Type

from dataclass_wizard import property_wizard

from app.core.enums import IntentEnum


@dataclass
class AbstractState(metaclass=property_wizard):
    pass


@dataclass
class ListMoviesState(AbstractState):
    date: str
    from_hour: str
    to_hour: str
    genre: str


@dataclass
class BuyTicketState(AbstractState):
    movie_title: str
    date_of_play: str
    hour_of_play: str
    number_of_tickets: int
    with_discount: bool
    seats_numbers: List[int]

    @property  # type: ignore
    def number_of_tickets(self) -> int:
        return self._number_of_tickets

    @number_of_tickets.setter
    def number_of_tickets(self, value: Any):
        self._number_of_tickets = -1
        try:
            self._number_of_tickets = int(value)
        except ValueError:
            logging.warn(f"Could not parse the number of tickets: {value}")

    @property  # type: ignore
    def with_discount(self) -> bool:
        return self._with_discount

    @with_discount.setter
    def with_discount(self, value: Any):
        self._with_discount = False
        if value in {"True", "true", "Yes", "yes"}:
            self._with_discount = True

    @property  # type: ignore
    def seats_numbers(self) -> List[int]:
        return self._seats_numbers

    @with_discount.setter
    def seats_numbers(self, raw_values: Any):
        self._seats_numbers = [-1]
        values: List[Any] = raw_values.split(", ")
        try:
            self._seats_numbers = [int(x) for x in values]
        except ValueError:
            logging.warn(f"Could not parse the number of seats: {values}")


@dataclass
class MovieSummaryState(AbstractState):
    title: str
    director: str
    year: int

    @property  # type: ignore
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: Any):
        self._year = -1
        try:
            self._year = int(value)
        except ValueError:
            logging.warn(f"Could not parse the year: {value}")


@dataclass
class CancelIntentState(AbstractState):
    pass


@dataclass
class CancelReservationState(AbstractState):
    title: str
    date: str
    hour: str
    seats_numbers: List[int]

    @property  # type: ignore
    def seats_numbers(self) -> List[int]:
        return self._seats_numbers

    @seats_numbers.setter
    def seats_numbers(self, raw_values: Any):
        self._seats_numbers = [-1]
        values: List[Any] = raw_values.split(", ")
        try:
            self._seats_numbers = [int(x) for x in values]
        except ValueError:
            logging.warn(f"Could not parse the number of seats: {values}")


intent_state_mapping: Dict[IntentEnum, Type[AbstractState]] = {
    IntentEnum.LIST_MOVIES: ListMoviesState,
    IntentEnum.BUY_TICKET: BuyTicketState,
    IntentEnum.MOVIE_SUMMARY: MovieSummaryState,
    IntentEnum.CANCEL_INTENT: CancelIntentState,
    IntentEnum.CANCEL_INTENT: CancelReservationState,
}
