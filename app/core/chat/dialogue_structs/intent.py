from enum import Enum


class IntentEnum(str, Enum):
    LIST_MOVIES = "prepare a list of movies"
    # BUY_TICKET = "buy a ticket for a show"
    # MOVIE_SUMMARY = "describe the movie"
    # CANCEL_INTENT = "cancel current procedure"
    # CANCEL_RESERVATION = "cancel reservation for the show"
    # INFO_ABOUT_POSSIBLE_SLOTS = "information about things the user can ask about"
    UNKNOWN = "unknown intent"
