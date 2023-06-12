from enum import Enum


class IntentEnum(Enum):
    # LIST_MOVIES = "prepare a list of movies"
    BOOK_TICKETS = "user want to book tickets for movie/list movies"
    SEE_BOOKING = "user want to access information regarding his already booked ticket"
    # GIVE_SUGGESTIONS = "provide user with information on what he can do or ask for"
    AFFIRMATIVE = "user in the affirmative"
    NEGATIVE = "user in the negative"
    UNKNOWN = "unknown intent"
