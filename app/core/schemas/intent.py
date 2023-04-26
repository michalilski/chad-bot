from enum import Enum


class IntentEnum(str, Enum):
    LIST_MOVIES = "prepare a list of movies"
    BUY_TICKET = "buy a ticket for a show"
    MOVIE_SUMMARY = "describe the movie"
    CANCEL_INTEN = "cancel current procedure"
    CANCEL_RESERVATION = "cancel reservation for the show"
