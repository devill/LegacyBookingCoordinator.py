"""Test for BookingCoordinatorImpl using ApprovalTests."""

from datetime import datetime

from approvaltests import verify
from global_object_factory import set_one, context

from legacy_booking.booking_coordinator_impl import BookingCoordinatorImpl


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

        # Act
        coordinator = BookingCoordinatorImpl()
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