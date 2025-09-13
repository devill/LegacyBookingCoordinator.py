"""Interface for partner notification operations."""

from abc import ABC, abstractmethod
from decimal import Decimal


class PartnerNotifier(ABC):
    """Abstract interface for partner notification operations."""

    @abstractmethod
    def notify_partner_about_booking(
        self,
        airline_code: str,
        booking_reference: str,
        total_price: Decimal,
        passenger_name: str,
        flight_details: str,
        is_rebooking: bool = False,
    ) -> None:
        """Notify partner about a booking."""
        pass

    @abstractmethod
    def validate_and_notify_special_requests(
        self, airline_code: str, special_requests: str, booking_ref: str
    ) -> bool:
        """Validate and notify about special requests."""
        pass

    @abstractmethod
    def update_partner_booking_status(
        self, airline_code: str, booking_ref: str, new_status: str
    ) -> None:
        """Update booking status with partner."""
        pass