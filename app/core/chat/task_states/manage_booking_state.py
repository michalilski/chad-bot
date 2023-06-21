from dataclasses import dataclass
from typing import Tuple, cast

from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.task_states import TaskState
from app.core.db.db_bridge import DatabaseBridge

TaksCompleted = bool


@dataclass
class ManageBookingState(TaskState):
    def __init__(self):
        super().__init__(
            [
                SlotMapping(
                    name="4_digit_pin",
                    description="4 digit pin number like 1234, 8710, 1890",
                    _info_template="There is a booking for the pin {}",
                    _request_template="What is the pin number that you got when making the reservation?",
                    is_required=True,
                ),
                SlotMapping(
                    name="surname",
                    description="surname used to book the ticket",
                    _info_template="The surname for the booking is {}",
                    _request_template="Under what surname was the ticket booked?",
                    is_required=False,
                ),
            ]
        )

    def generate_suggestions_outline(self) -> str:
        return (
            "I am now helping you to get your booking details."
            "To get this information please provide your reservation PIN code."
        )

    def generate_next_response(self) -> Tuple[str, TaksCompleted]:
        try:
            int_pin = self["4_digit_pin"].value
        except ValueError:
            self["4_digit_pin"].set_certain_values([])

        if self["4_digit_pin"].is_empty:
            return "Please give me the pin that you received when booking the ticket", TaksCompleted(False)

        pin: str = cast(str, self["4_digit_pin"].value)
        tickets = DatabaseBridge.get_bookings_for_pin(pin)

        if len(tickets) == 0:
            return f"There are no tickets booked for pin {pin}. Please make sure your pin is correct.", TaksCompleted(
                True
            )
        return f"Under the pin code {pin} there is a booking for {tickets[-1].show}", TaksCompleted(True)
