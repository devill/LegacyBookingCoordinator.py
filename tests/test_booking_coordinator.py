"""Test for BookingCoordinatorImpl using ApprovalTests."""

import random
from datetime import datetime
from typing import Dict, Any, List, Optional

from approvaltests import verify
from specrec import set_one, context

from legacy_booking.audit_logger import AuditLogger
from legacy_booking.audit_logger_impl import AuditLoggerImpl
from legacy_booking.booking_coordinator_impl import BookingCoordinatorImpl
from legacy_booking.booking_repository import BookingRepository
from legacy_booking.booking_repository_impl import BookingRepositoryImpl
from legacy_booking.flight_availability_service import FlightAvailabilityService
from legacy_booking.flight_availability_service_impl import FlightAvailabilityServiceImpl
from legacy_booking.partner_notifier import PartnerNotifier
from legacy_booking.partner_notifier_impl import PartnerNotifierImpl


class TestBookingCoordinator:
    """Test class for BookingCoordinatorImpl."""

    def test_book_flight_should_create_booking_successfully(self) -> None:
        """Test that booking flight creates booking successfully."""
        # Arrange
        passenger_name = "John Doe"
        flight_number = "AA123"
        departure_date = datetime(2025, 7, 3, 12, 42, 11)
        passenger_count = 2
        airline_code = "AA"
        special_requests = "meal,wheelchair"
        booking_date = datetime(2025, 3, 4, 14, 0, 56)

        with context():
            set_one(BookingRepositoryImpl, BookingRepositoryStub())
            set_one(FlightAvailabilityServiceImpl, FlightAvailabilityServiceStub())
            set_one(PartnerNotifierImpl, PartnerNotifierStub())
            set_one(AuditLoggerImpl, AuditLoggerStub())
            set_one(random.Random, RandomStub())

            # Act
            coordinator = BookingCoordinatorImpl(booking_date)
            result = coordinator.book_flight(
                passenger_name,
                flight_number,
                departure_date,
                passenger_count,
                airline_code,
                special_requests,
            )

            # Assert
            verify(f"Returns: \"{result}\"")


class AuditLoggerStub(AuditLogger):
    """Stub implementation for AuditLogger."""

    def log_booking_activity(self, activity: str, booking_reference: str, user_info: str) -> None:
        """Log booking activity - stub implementation."""
        pass

    def record_pricing_calculation(self, calculation_details: str, final_price: float, flight_info: str) -> None:
        """Record pricing calculation - stub implementation."""
        pass

    def log_error_with_alert(self, ex: Exception, context: str, booking_ref: str) -> None:
        """Log error with alert - stub implementation."""
        raise NotImplementedError()

    def flush_and_archive_logs(self) -> None:
        """Flush and archive logs - stub implementation."""
        raise NotImplementedError()


class PartnerNotifierStub(PartnerNotifier):
    """Stub implementation for PartnerNotifier."""

    def notify_partner_about_booking(
        self,
        airline_code: str,
        booking_reference: str,
        total_price: float,
        passenger_name: str,
        flight_details: str,
        is_rebooking: bool = False,
    ) -> None:
        """Notify partner about booking - stub implementation."""
        pass

    def validate_and_notify_special_requests(
        self, airline_code: str, special_requests: str, booking_ref: str
    ) -> bool:
        """Validate and notify special requests - stub implementation."""
        return True

    def update_partner_booking_status(
        self, airline_code: str, booking_ref: str, new_status: str
    ) -> None:
        """Update partner booking status - stub implementation."""
        pass


class FlightAvailabilityServiceStub(FlightAvailabilityService):
    """Stub implementation for FlightAvailabilityService."""

    def check_and_get_available_seats_for_booking(
        self, flight_number: str, departure_date: datetime, passenger_count: int
    ) -> List[str]:
        """Check and get available seats - stub implementation."""
        return ["11A", "11B"]

    def is_flight_fully_booked(self, flight_number: str, departure_date: datetime) -> bool:
        """Check if flight is fully booked - stub implementation."""
        raise NotImplementedError()


class BookingRepositoryStub(BookingRepository):
    """Stub implementation for BookingRepository."""

    def save_booking_details(
        self, passenger_name: str, flight_details: str, price: float, booking_date: datetime
    ) -> str:
        """Save booking details - stub implementation."""
        return "APPLE3.14"

    def get_booking_info(self, booking_reference: str) -> Dict[str, Any]:
        """Get booking info - stub implementation."""
        raise NotImplementedError()

    def validate_and_enrich_booking_data(
        self, booking_ref: str
    ) -> tuple[bool, Optional[float], Optional[str]]:
        """Validate and enrich booking data - stub implementation."""
        raise NotImplementedError()

    def get_historical_pricing_data(
        self, flight_number: str, date: datetime, day_range: int
    ) -> float:
        """Get historical pricing data - stub implementation."""
        raise NotImplementedError()


class RandomStub(random.Random):
    """Stub implementation for Random that returns deterministic values."""

    def randint(self, a: int, b: int) -> int:
        """Return deterministic value for randint."""
        return 3