from enum import Enum


class IntentEnum(Enum):
    BOOK_TICKETS = "user want to book tickets for movie/list movies"
    SEE_BOOKING = "user want to access information regarding his already booked ticket"
    # GIVE_SUGGESTIONS = "provide user with information on what he can do or ask for"
    AFFIRMATIVE = "user responds in the affirmative"
    NEGATIVE = "user responds in the negative"
    CANCEL_PROCEDURE = "user wants to do something different"
    UNKNOWN = "unknown intent"
