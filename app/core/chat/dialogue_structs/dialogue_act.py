from enum import Enum


class DialogueActEnum(str, Enum):
    REQUEST = "request for a value of slot"
    INFORM = "give a value of slot"
    CONFIRM = "confirm value of slot"
    WRITE_MESSAGE = "write given message"

