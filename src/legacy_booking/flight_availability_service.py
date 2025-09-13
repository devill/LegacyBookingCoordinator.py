"""Interface for flight availability operations."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class FlightAvailabilityService(ABC):
    """Abstract interface for flight availability operations."""

    @abstractmethod
    def check_and_get_available_seats_for_booking(
        self, flight_number: str, departure_date: datetime, passenger_count: int
    ) -> List[str]:
        """Check and get available seats for booking."""
        pass

    @abstractmethod
    def is_flight_fully_booked(
        self, flight_number: str, departure_date: datetime
    ) -> bool:
        """Check if flight is fully booked."""
        pass