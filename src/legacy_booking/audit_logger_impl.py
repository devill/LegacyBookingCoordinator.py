"""Audit logger implementation."""

from decimal import Decimal

from .audit_logger import AuditLogger
from .can_not_use_in_tests_exception import CanNotUseInTestsException


class AuditLoggerImpl(AuditLogger):
    """Production audit logger implementation - cannot be used in tests."""

    def __init__(self, log_directory: str, verbose_mode: bool) -> None:
        raise CanNotUseInTestsException("AuditLoggerImpl")

    def log_booking_activity(
        self, activity: str, booking_reference: str, user_info: str
    ) -> None:
        raise CanNotUseInTestsException("AuditLoggerImpl")

    def record_pricing_calculation(
        self, calculation_details: str, final_price: Decimal, flight_info: str
    ) -> None:
        raise CanNotUseInTestsException("AuditLoggerImpl")

    def log_error_with_alert(
        self, ex: Exception, context: str, booking_ref: str
    ) -> None:
        raise CanNotUseInTestsException("AuditLoggerImpl")

    def flush_and_archive_logs(self) -> None:
        raise CanNotUseInTestsException("AuditLoggerImpl")