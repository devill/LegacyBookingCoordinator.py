"""Booking repository implementation."""

from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Tuple

from .booking_repository import BookingRepository
from .can_not_use_in_tests_exception import CanNotUseInTestsException


class BookingRepositoryImpl(BookingRepository):
    """Production booking repository - cannot be used in tests."""

    def __init__(self, db_connection_string: str, max_retries: int) -> None:
        raise CanNotUseInTestsException("BookingRepositoryImpl")

    def save_booking_details(
        self, passenger_name: str, flight_details: str, price: Decimal, booking_date: datetime
    ) -> str:
        raise CanNotUseInTestsException("BookingRepositoryImpl")

    def get_booking_info(self, booking_reference: str) -> Dict[str, Any]:
        raise CanNotUseInTestsException("BookingRepositoryImpl")

    def validate_and_enrich_booking_data(
        self, booking_ref: str
    ) -> Tuple[bool, Decimal, str]:
        raise CanNotUseInTestsException("BookingRepositoryImpl")

    def get_historical_pricing_data(
        self, flight_number: str, date: datetime, day_range: int
    ) -> Decimal:
        raise CanNotUseInTestsException("BookingRepositoryImpl")