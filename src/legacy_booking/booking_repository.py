"""Interface for booking repository operations."""

from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Tuple


class BookingRepository(ABC):
    """Abstract interface for booking repository operations."""

    @abstractmethod
    def save_booking_details(
        self, passenger_name: str, flight_details: str, price: Decimal, booking_date: datetime
    ) -> str:
        """Save booking details and return booking reference."""
        pass

    @abstractmethod
    def get_booking_info(self, booking_reference: str) -> Dict[str, Any]:
        """Retrieve booking information."""
        pass

    @abstractmethod
    def validate_and_enrich_booking_data(
        self, booking_ref: str
    ) -> Tuple[bool, Decimal, str]:
        """Validate and enrich booking data. Returns (success, actual_price, enriched_info)."""
        pass

    @abstractmethod
    def get_historical_pricing_data(
        self, flight_number: str, date: datetime, day_range: int
    ) -> Decimal:
        """Get historical pricing data."""
        pass