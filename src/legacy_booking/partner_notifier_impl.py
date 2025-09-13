"""Partner notifier implementation."""

from decimal import Decimal

from .partner_notifier import PartnerNotifier
from .can_not_use_in_tests_exception import CanNotUseInTestsException


class PartnerNotifierImpl(PartnerNotifier):
    """Production partner notifier - cannot be used in tests."""

    def __init__(self, smtp_server: str, use_encryption: bool) -> None:
        raise CanNotUseInTestsException("PartnerNotifierImpl")

    def notify_partner_about_booking(
        self,
        airline_code: str,
        booking_reference: str,
        total_price: Decimal,
        passenger_name: str,
        flight_details: str,
        is_rebooking: bool = False,
    ) -> None:
        raise CanNotUseInTestsException("PartnerNotifierImpl")

    def validate_and_notify_special_requests(
        self, airline_code: str, special_requests: str, booking_ref: str
    ) -> bool:
        raise CanNotUseInTestsException("PartnerNotifierImpl")

    def update_partner_booking_status(
        self, airline_code: str, booking_ref: str, new_status: str
    ) -> None:
        raise CanNotUseInTestsException("PartnerNotifierImpl")