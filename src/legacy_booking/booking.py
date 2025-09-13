"""Booking data class."""

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Booking:
    """Represents a flight booking."""

    booking_reference: str
    passenger_name: str
    flight_number: str
    departure_date: datetime
    passenger_count: int
    airline_code: str
    final_price: Decimal
    special_requests: str
    booking_date: datetime
    status: str

    def __str__(self) -> str:
        """Return formatted booking details."""
        result = []
        formatter = lambda dt: dt.strftime("%Y-%m-%d %H:%M")

        result.append(f"New booking: {self.booking_reference}")
        result.append(f"  👤 {self.passenger_name}")
        result.append(f"  ✈️ {self.flight_number}")
        result.append(f"  📅 {formatter(self.departure_date)}")
        result.append(f"  👥 {self.passenger_count}")
        result.append(f"  🏢 {self.airline_code}")
        result.append(f"  💰 ${self.final_price:.2f}")

        if self.special_requests:
            result.append(f"  🎯 {self.special_requests}")

        result.append(f"  📝 {formatter(self.booking_date)}")
        result.append(f"  ✅ {self.status}")

        return "\n".join(result)