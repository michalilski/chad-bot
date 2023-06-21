from enum import Enum


class IntentEnum(Enum):
    BOOK_TICKETS = "user want to book tickets for movie/list movies"
    SEE_BOOKING = "user want to access information regarding his already booked ticket"
    CANCEL_BOOKING = "user want to cancel his already booked ticket"
    AFFIRMATIVE = "user responds in the affirmative"
    UNKNOWN = "unknown intent"
