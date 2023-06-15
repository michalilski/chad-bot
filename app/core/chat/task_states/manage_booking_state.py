from dataclasses import dataclass

from app.core.chat.dialogue_structs.slot_mapping import SlotMapping
from app.core.chat.task_states import TaskState
from app.core.db.db_bridge import DatabaseBridge


@dataclass
class ManageBookingState(TaskState):
    def __init__(self):
        super().__init__(
            [
                SlotMapping(
                    name="pin",
                    description="pin code that the user provided",
                    _info_template="The pin is {}",
                    _request_template="What is the pin number that you got when making the reservation?",
                    is_required=True,
                ),
            ]
        )

    def generate_suggestions_outline(self) -> str:
        return "You need to provide a pin number in order to manage your booking"

    def generate_next_response(self) -> str:
        try:
            int_pin = self["pin"].value
        except ValueError:
            self["pin"].set_certain_values([])

        if self["pin"].is_empty:
            return "Please give me the pin that you received when booking the ticket"

        pin = self["pin"].value
        tickets = DatabaseBridge.get_bookings_for_pin(pin)

        if len(tickets) == 0:
            return f"There are no tickets booked for pin {pin}. Please make sure your pin is correct."

        tickets = tickets[-1:]
        if len(tickets) == 1:
            return f"There is a booking under {pin} for {tickets[0].show}"
