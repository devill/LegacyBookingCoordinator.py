"""Interface for audit logging operations."""

from abc import ABC, abstractmethod
from decimal import Decimal


class AuditLogger(ABC):
    """Abstract interface for audit logging operations."""

    @abstractmethod
    def log_booking_activity(
        self, activity: str, booking_reference: str, user_info: str
    ) -> None:
        """Log a booking activity."""
        pass

    @abstractmethod
    def record_pricing_calculation(
        self, calculation_details: str, final_price: Decimal, flight_info: str
    ) -> None:
        """Record details of pricing calculations."""
        pass

    @abstractmethod
    def log_error_with_alert(
        self, ex: Exception, context: str, booking_ref: str
    ) -> None:
        """Log an error with alerting."""
        pass

    @abstractmethod
    def flush_and_archive_logs(self) -> None:
        """Flush and archive current logs."""
        pass