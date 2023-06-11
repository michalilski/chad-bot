import logging

# @dataclass
# class BuyTicketState(AbstractState):
#     movie_title: Optional[str] = None
#     date_of_play: Optional[str] = None
#     hour_of_play: Optional[str] = None
#     number_of_tickets: Optional[int] = None
#     seats_numbers: Optional[List[int]] = None
#     required: Tuple[str, ...] = ("movie_title", "date_of_play")
#
#     @property  # type: ignore
#     def number_of_tickets(self) -> Optional[int]:
#         return self._number_of_tickets
#
#     @number_of_tickets.setter
#     def number_of_tickets(self, value: Any):
#         self._number_of_tickets = None
#         try:
#             self._number_of_tickets = int(value)
#         except ValueError:
#             logging.warn(f"Could not parse the number of tickets: {value}")
#         except TypeError:
#             pass
#
#     @property  # type: ignore
#     def seats_numbers(self) -> Optional[List[int]]:
#         return self._seats_numbers
#
#     @seats_numbers.setter
#     def seats_numbers(self, raw_values: Any):
#         self._seats_numbers = None
#         try:
#             values: List[Any] = raw_values.split(", ")
#             self._seats_numbers = [int(x) for x in values]
#         except ValueError:
#             logging.warn(f"Could not parse the number of seats: {raw_values}")
#         except AttributeError:
#             pass


# @dataclass
# class MovieSummaryState(AbstractState):
#     title: Optional[str] = None
#     director: Optional[str] = None
#     year: Optional[int] = None
#     required: Tuple[str, ...] = ("title",)
#
#     @property  # type: ignore
#     def year(self) -> Optional[int]:
#         return self._year
#
#     @year.setter
#     def year(self, value: Any):
#         self._year = None
#         try:
#             self._year = int(value)
#         except ValueError:
#             logging.warn(f"Could not parse the year: {value}")
#         except TypeError:
#             pass


# @dataclass
# class CancelIntentState(AbstractState):
#     pass


# @dataclass
# class CancelReservationState(AbstractState):
#     title: Optional[str] = None
#     date: Optional[str] = None
#     hour: Optional[str] = None
#     seats_numbers: Optional[List[str]] = None
#     required: Tuple[str, ...] = ("title", "date", "hour", "seats_numbers")
#
#     @property  # type: ignore
#     def seats_numbers(self) -> Optional[List[int]]:
#         return self._seats_numbers
#
#     @seats_numbers.setter
#     def seats_numbers(self, raw_values: Any):
#         self._seats_numbers = None
#         try:
#             values: List[Any] = raw_values.split(", ")
#             self._seats_numbers = [int(x) for x in values]
#         except ValueError:
#             logging.warn(f"Could not parse the number of seats: {raw_values}")
#         except AttributeError:
#             pass


# @dataclass
# class UnknownIntentState(AbstractState):
#     pass



