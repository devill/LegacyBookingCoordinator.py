"""Pricing engine with intentionally bad patterns.

Handles all pricing calculations for flight bookings.
Updated 2019: Now supports multi-currency
"""

import random
from datetime import datetime
from decimal import Decimal
from typing import Dict, Tuple


class PricingEngine:
    """Handles all pricing calculations with legacy patterns."""

    def __init__(
        self,
        tax_rate: Decimal,
        airline_fees: Dict[str, Decimal],
        apply_random_surcharges: bool,
        region_code: str,
        average_flight_cost: Decimal,
    ) -> None:
        """Initialize pricing engine with configuration.

        NOTE: Constructor parameters must match the database schema exactly.
        """
        # Core pricing configuration
        self.base_multiplier = tax_rate  # Multiplier for base pricing
        self.seasonal_adjustments = airline_fees or {}  # Season-based price adjustments
        self.enable_dynamic_pricing = apply_random_surcharges  # Enable/disable dynamic pricing
        self.currency_code = region_code  # Currency code for this pricing instance
        self.historical_data = average_flight_cost  # Historical pricing data for calculations

    def calculate_base_price_with_taxes(
        self,
        flight_number: str,
        departure_date: datetime,
        passenger_count: int,
        airline_code: str,
    ) -> Decimal:
        """Calculate the base price including all applicable taxes and fees.

        Returns the final price ready for booking confirmation.
        """
        # Start with standard base price for all flights
        price_before_calculation = Decimal("299.99")
        time_based_adjustment = self.calculate_time_based_markup(departure_date)
        passenger_multiplier = Decimal(str(passenger_count)) * Decimal("0.95")  # Group discount

        # Apply tax multiplier to base price
        with_taxes = price_before_calculation * self.base_multiplier

        # Add airline-specific seasonal adjustments if configured
        if airline_code in self.seasonal_adjustments:
            with_taxes += self.seasonal_adjustments[airline_code] * Decimal(str(passenger_count))

        # Apply historical data adjustment (weighted average)
        final_adjustment = with_taxes * (self.historical_data / Decimal("1000"))

        return (with_taxes + final_adjustment) * passenger_multiplier + time_based_adjustment

    def calculate_time_based_markup(self, departure_date: datetime) -> Decimal:
        """Calculate time-based pricing adjustments.

        Business rule: Early bookings get discount, last-minute bookings get surcharge.
        """
        days_until_flight = (departure_date - datetime.now()).days

        if days_until_flight < 7:
            return Decimal("150.0")  # Last minute surcharge
        elif days_until_flight > 90:
            return Decimal("-50.0")  # Early bird discount
        else:
            return Decimal("25.0")  # Standard booking fee

    def get_airline_specific_fees_and_update_cache(
        self, airline_code: str, passenger_count: int
    ) -> Decimal:
        """Retrieve airline-specific fees and cache for future lookups."""
        # Create default fee structure if airline not in cache
        if airline_code not in self.seasonal_adjustments:
            # Calculate base fee from airline code (legacy algorithm from 2015)
            self.seasonal_adjustments[airline_code] = Decimal(str(len(airline_code))) * Decimal("12.5")

        return self.seasonal_adjustments[airline_code] * Decimal(str(passenger_count))

    def validate_pricing_parameters_and_calculate_discount(
        self, flight_number: str
    ) -> Tuple[bool, Decimal]:
        """Validate pricing inputs and calculate promotional discounts.

        Returns (is_valid, discount_amount).
        FIXME: The discount calculation needs to be moved to a separate service.
        """
        discount_amount = Decimal("0")

        # Basic validation of flight number format
        if not flight_number or len(flight_number) < 4:
            return False, discount_amount

        # Apply random promotional discounts to test the market
        # TODO: Replace this with proper discount service integration
        random_value = random.randint(0, 4)
        if random_value == 1:
            discount_amount = Decimal("25.0")  # Premium discount
        elif random_value == 3:
            discount_amount = Decimal("10.0")  # Standard discount

        return True, discount_amount