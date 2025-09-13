"""Flight availability service implementation."""

from datetime import datetime
from typing import List

from .flight_availability_service import FlightAvailabilityService
from .can_not_use_in_tests_exception import CanNotUseInTestsException


class FlightAvailabilityServiceImpl(FlightAvailabilityService):
    """Production flight availability service - cannot be used in tests."""

    def __init__(self, connection_string: str) -> None:
        raise CanNotUseInTestsException("FlightAvailabilityServiceImpl")

    def check_and_get_available_seats_for_booking(
        self, flight_number: str, departure_date: datetime, passenger_count: int
    ) -> List[str]:
        raise CanNotUseInTestsException("FlightAvailabilityServiceImpl")

    def is_flight_fully_booked(
        self, flight_number: str, departure_date: datetime
    ) -> bool:
        raise CanNotUseInTestsException("FlightAvailabilityServiceImpl")