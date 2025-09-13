"""
Legacy Booking Coordinator - A Code Kata for Testing Legacy Systems

WARNING: This code intentionally demonstrates bad practices and anti-patterns
for educational purposes. Do not use these patterns in production code!
"""

__version__ = "1.0.0"

from .booking import Booking
from .booking_coordinator_impl import BookingCoordinatorImpl
from .can_not_use_in_tests_exception import CanNotUseInTestsException

__all__ = [
    "Booking",
    "BookingCoordinatorImpl",
    "CanNotUseInTestsException",
]