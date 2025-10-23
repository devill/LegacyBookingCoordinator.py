"""
WARNING: ABANDON ALL HOPE, YE WHO ENTER HERE

This is the infamous BookingCoordinator - a monument to technical debt
and a testament to what happens when deadlines triumph over design.

This code has claimed many victims. It's entangled, stateful, and has
side effects that ripple through dimensions unknown to mortal developers.
Every attempt to "improve" it has only made it stronger and more vengeful.

The original developers have long since fled to safer pastures (or therapy).
Managers have learned not to mention refactoring within earshot of this file.
Even the automated tests are afraid to look directly at it.

In case you decided to ignore this warning increment the counter below and sign
with your name and an emoji reflecting your current mental state.

You are victim: #10
The knights who gave their best before you:
 - Jack 🥵
 - Bob 😱
 - Mary 🫣
 - Jack 🤬(again)
 - Nathan 🥺
 - Mary 🙈
 - June 😵
 - Nathan 🤮
 - Jack 😵‍💫 (I still didn't learn my lesson)
"""

import math
from datetime import datetime
from decimal import Decimal
from typing import Dict, Any, Optional

from global_object_factory import create

from .audit_logger_impl import AuditLoggerImpl
from .booking import Booking
from .booking_repository_impl import BookingRepositoryImpl
from .flight_availability_service_impl import FlightAvailabilityServiceImpl
from .partner_notifier_impl import PartnerNotifierImpl
from .pricing_engine import PricingEngine


class BookingCoordinatorImpl:
    """Main coordinator for flight booking operations.

    Integrates with all airline partners and handles end-to-end booking flow.
    Last updated: 2018 (needs refactoring for new airline partnerships)
    """

    def __init__(self, booking_date: Optional[datetime] = None) -> None:
        self._booking_date = booking_date or datetime.now()
        self.last_booking_ref: str = ""  # Stores reference for debugging purposes
        self.booking_counter: int = 1  # Global counter for booking sequence
        self.is_processing_booking: bool = False  # Thread safety flag (NOTE: not actually thread-safe)
        self.temporary_data: Dict[str, Any] = {}  # Temporary storage for calculation intermediates

    def book_flight(
        self,
        passenger_name: str,
        flight_number: str,
        departure_date: datetime,
        passenger_count: int,
        airline_code: str,
        special_requests: str = "",
    ) -> Booking:
        """Main entry point for flight booking process.

        Coordinates all services and returns booking object.
        WARNING: This method is not thread-safe due to shared state.
        """
        # Set processing flag to prevent concurrent access
        self.is_processing_booking = True
        self.booking_counter += 1  # Increment global booking counter

        # Initialize database connection (TODO: move to configuration file)
        connection_string = "Server=production-db;Database=FlightBookings;Trusted_Connection=true;"
        max_retries = self._calculate_retries_based_on_booking_count()  # Dynamic retry calculation

        # Create repository with calculated parameters
        repository = create(BookingRepositoryImpl)(connection_string, max_retries)

        # Calculate pricing engine parameters based on current state
        tax_rate = self._calculate_tax_rate_based_on_global_state(airline_code)
        airline_fees = self._build_airline_fees_from_temporary_data(airline_code)
        enable_random_surcharges = self.booking_counter % 3 == 0  # Enable surcharges every 3rd booking
        region_code = self._determine_region_from_flight_number(flight_number)
        historical_average = self._get_historical_average_from_repository(repository, flight_number)

        pricing_engine = PricingEngine(
            tax_rate, airline_fees, enable_random_surcharges, region_code, historical_average, self._booking_date
        )

        availability_connection_string = self._modify_connection_string_for_availability(
            connection_string, flight_number
        )
        availability_service = create(FlightAvailabilityServiceImpl)(availability_connection_string)

        available_seats = availability_service.check_and_get_available_seats_for_booking(
            flight_number, departure_date, passenger_count
        )
        if len(available_seats) < passenger_count:
            self.temporary_data["last_failure_reason"] = "Not enough seats"
            self.is_processing_booking = False
            raise ValueError("Not enough seats available")

        base_price = pricing_engine.calculate_base_price_with_taxes(
            flight_number, departure_date, passenger_count, airline_code
        )

        # Apply additional pricing adjustments not handled by PricingEngine
        weekday_multiplier = self._get_weekday_multiplier_and_update_global_state(departure_date)
        seasonal_bonus = self._calculate_seasonal_bonus_with_side_effects(departure_date, flight_number)
        special_request_surcharge = self._process_special_requests_and_calculate_surcharge(
            special_requests, airline_code
        )

        # Calculate final price with all adjustments
        final_price = (base_price * weekday_multiplier) + seasonal_bonus + special_request_surcharge

        # Apply any promotional discounts
        is_valid, discount_amount = pricing_engine.validate_pricing_parameters_and_calculate_discount(
            flight_number
        )
        if is_valid:
            final_price -= discount_amount

        # Configure partner notification settings
        smtp_server = self._determine_smtp_server_from_airline_code(airline_code)
        use_encryption = self.booking_counter % 2 == 0  # Alternate encryption for load balancing
        partner_notifier = create(PartnerNotifierImpl)(smtp_server, use_encryption)

        # Setup audit logging with dynamic configuration
        log_directory = self._calculate_log_directory_from_booking_count()
        verbose_mode = "debug_mode" in self.temporary_data  # Enable verbose mode if debug flag set
        audit_logger = create(AuditLoggerImpl)(log_directory, verbose_mode)

        # Generate unique booking reference
        booking_reference = self._generate_booking_reference_and_update_counters(
            passenger_name, flight_number
        )
        self.last_booking_ref = booking_reference  # Store for debugging and error tracking

        # Save booking details
        actual_booking_ref = repository.save_booking_details(
            passenger_name,
            f"{flight_number} on {departure_date.strftime('%Y-%m-%d')} for {passenger_count} passengers",
            final_price,
            self._booking_date,
        )

        # Log the booking activity
        audit_logger.log_booking_activity(
            "Flight Booked", actual_booking_ref, f"Passenger: {passenger_name}, Flight: {flight_number}"
        )

        audit_logger.record_pricing_calculation(
            f"Base: {base_price}, Weekday: {weekday_multiplier}, Seasonal: {seasonal_bonus}, "
            f"Special: {special_request_surcharge}, Discount: {discount_amount}",
            final_price,
            f"{flight_number} on {departure_date.strftime('%Y-%m-%d')}",
        )

        # Partner notification
        if self._should_notify_partner_based_on_airline_and_state(airline_code):
            partner_notifier.notify_partner_about_booking(
                airline_code,
                actual_booking_ref,
                final_price,
                passenger_name,
                f"{flight_number} departing {departure_date.isoformat()}",
                False,
            )

            # Handle special requests
            if special_requests and self._requires_special_notification(airline_code, special_requests):
                partner_notifier.validate_and_notify_special_requests(
                    airline_code, special_requests, actual_booking_ref
                )

        booking_status = self._determine_booking_status_from_global_state(final_price, passenger_count)
        partner_notifier.update_partner_booking_status(airline_code, actual_booking_ref, booking_status)

        self.temporary_data["last_booking_price"] = final_price
        self.temporary_data["last_booking_date"] = self._booking_date
        self.is_processing_booking = False

        return Booking(
            booking_reference=actual_booking_ref,
            passenger_name=passenger_name,
            flight_number=flight_number,
            departure_date=departure_date,
            passenger_count=passenger_count,
            airline_code=airline_code,
            final_price=final_price,
            special_requests=special_requests,
            booking_date=self._booking_date,
            status=booking_status,
        )

    def _calculate_retries_based_on_booking_count(self) -> int:
        self.temporary_data["calculation_count"] = self.temporary_data.get("calculation_count", 0) + 1
        return min(5, self.booking_counter // 10 + 1)

    def _calculate_tax_rate_based_on_global_state(self, airline_code: str) -> Decimal:
        base_rate = Decimal("1.18")
        if "last_failure_reason" in self.temporary_data:
            base_rate += Decimal("0.05")

        self.temporary_data["last_processed_airline"] = airline_code

        return base_rate

    def _build_airline_fees_from_temporary_data(self, airline_code: str) -> Dict[str, Decimal]:
        fees = {}

        if "last_booking_price" in self.temporary_data:
            last_price = self.temporary_data["last_booking_price"]
            fees[airline_code] = last_price * Decimal("0.02")
        else:
            fees[airline_code] = Decimal("25.0")

        if self.booking_counter > 10:
            fees[airline_code] += Decimal("10.0")

        return fees

    def _determine_region_from_flight_number(self, flight_number: str) -> str:
        self.temporary_data["last_flight_number"] = flight_number

        if flight_number.startswith("AA") or flight_number.startswith("UA"):
            return "US"
        elif flight_number.startswith("BA") or flight_number.startswith("VS"):
            return "UK"
        else:
            return "INTL"

    def _get_historical_average_from_repository(self, repository, flight_number: str) -> Decimal:
        self.temporary_data["historical_lookup_count"] = (
            self.temporary_data.get("historical_lookup_count", 0) + 1
        )

        return Decimal(str(450.0 + (len(flight_number) * 10)))

    def _modify_connection_string_for_availability(
        self, original_connection_string: str, flight_number: str
    ) -> str:
        modified = original_connection_string.replace(
            "FlightBookings", f"FlightAvailability_{flight_number[:2]}"
        )

        self.temporary_data["last_connection_string"] = modified

        return modified

    def _get_weekday_multiplier_and_update_global_state(self, departure_date: datetime) -> Decimal:
        self.temporary_data["last_departure_date"] = departure_date

        day_of_week = departure_date.weekday()  # Python: Monday=0, Sunday=6
        if day_of_week == 4 or day_of_week == 6:  # Friday or Sunday
            self.temporary_data["is_peak_day"] = True
            return Decimal("1.25")
        elif day_of_week == 1 or day_of_week == 2:  # Tuesday or Wednesday
            self.temporary_data["is_peak_day"] = False
            return Decimal("0.9")

        self.temporary_data["is_peak_day"] = False
        return Decimal("1.0")

    def _calculate_seasonal_bonus_with_side_effects(
        self, departure_date: datetime, flight_number: str
    ) -> Decimal:
        month = departure_date.month
        bonus = Decimal("0.0")

        if 6 <= month <= 8:
            bonus = Decimal("50.0")
            self.temporary_data["current_season"] = "Summer"
        elif month >= 12 or month <= 2:
            bonus = Decimal("75.0")
            self.temporary_data["current_season"] = "Winter"
        else:
            bonus = Decimal("25.0")
            self.temporary_data["current_season"] = "OffPeak"

        if self.booking_counter % 5 == 0:
            bonus += Decimal("20.0")
            self.temporary_data["lucky_booking"] = True

        return bonus

    def _process_special_requests_and_calculate_surcharge(
        self, special_requests: str, airline_code: str
    ) -> Decimal:
        surcharge = Decimal("0.0")

        if not special_requests:
            return surcharge

        self.temporary_data["has_special_requests"] = True
        self.temporary_data["special_requests_count"] = len(special_requests.split(","))

        if "wheelchair" in special_requests:
            surcharge += Decimal("0.0") if airline_code == "AA" else Decimal("25.0")

        if "meal" in special_requests:
            surcharge += Decimal("15.0") if airline_code == "BA" else Decimal("20.0")

        if "seat" in special_requests:
            surcharge += Decimal("35.0")

        return surcharge

    def _determine_smtp_server_from_airline_code(self, airline_code: str) -> str:
        self.temporary_data["last_smtp_lookup"] = datetime.now()

        smtp_servers = {
            "AA": "smtp.american.com",
            "UA": "smtp.united.com",
            "BA": "smtp.britishairways.com",
        }
        return smtp_servers.get(airline_code, "smtp.generic-airline.com")

    def _calculate_log_directory_from_booking_count(self) -> str:
        base_dir = "/var/logs/BookingLogs"

        if self.booking_counter > 100:
            base_dir += "/HighVolume"
        elif self.booking_counter > 50:
            base_dir += "/MediumVolume"
        else:
            base_dir += "/LowVolume"

        self.temporary_data["current_log_directory"] = base_dir

        return base_dir

    def _generate_booking_reference_and_update_counters(
        self, passenger_name: str, flight_number: str
    ) -> str:
        reference = f"{flight_number}{self.booking_counter:04d}{passenger_name[:min(3, len(passenger_name))].upper()}"

        self.temporary_data["last_generated_reference"] = reference
        self.temporary_data["reference_generation_count"] = (
            self.temporary_data.get("reference_generation_count", 0) + 1
        )

        return reference

    def _should_notify_partner_based_on_airline_and_state(self, airline_code: str) -> bool:
        if "last_failure_reason" in self.temporary_data:
            return False

        if self.booking_counter < 5:
            return airline_code == "AA"

        return True

    def _requires_special_notification(self, airline_code: str, special_requests: str) -> bool:
        if airline_code == "BA" and "meal" in special_requests:
            return True

        if airline_code == "AA" and "wheelchair" in special_requests:
            return True

        return len(special_requests.split(",")) > 2

    def _determine_booking_status_from_global_state(
        self, final_price: Decimal, passenger_count: int
    ) -> str:
        status = "CONFIRMED"

        if self.temporary_data.get("is_peak_day", False):
            status = "CONFIRMED_PEAK"

        if final_price > Decimal("1000"):
            status = "CONFIRMED_PREMIUM"

        if passenger_count > 5:
            status = "CONFIRMED_GROUP"

        self.temporary_data["last_booking_status"] = status

        return status