from dataclasses import dataclass
from typing import Dict, List, Type

from app.core.enums import IntentEnum


@dataclass
class AbstractState:
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


@dataclass
class MovieSummaryState(AbstractState):
    title: str
    year: int
    director: str


@dataclass
class CancelIntentState(AbstractState):
    pass


@dataclass
class CancelReservationState(AbstractState):
    title: str
    date: str
    hour: str
    seats_numbers: List[int]


intent_state_mapping: Dict[IntentEnum, Type[AbstractState]] = {
    IntentEnum.LIST_MOVIES: ListMoviesState,
    IntentEnum.BUY_TICKET: BuyTicketState,
    IntentEnum.MOVIE_SUMMARY: MovieSummaryState,
    IntentEnum.CANCEL_INTENT: CancelIntentState,
    IntentEnum.CANCEL_INTENT: CancelReservationState,
}
