# Code Kata: *Legacy Flight Booking System Testing*

# 🎯 Objective:

Introduce testability into an entangled legacy system responsible for managing flight bookings, pricing, and external integrations.

## 💼 Business Context:

Your company maintains a **legacy monolithic flight booking system**, originally written in a hurry for a client with ever-changing airline partnership rules. The original developers are long gone, and now you're tasked with adding **unit tests** and eventually decoupling and refactoring the system.

**Unfortunately:**

* Classes instantiate each other *directly* with `new` (well, direct instantiation in Python).
* Side effects (logging, emailing, pricing calls) happen all over the place.
* There is **no clean dependency injection**, no container, no interfaces (abstract base classes).
* Changes require fear-driven development, unless something changes…

### What the legacy code does

The booking system coordinates:

1. **FlightAvailabilityService**: Queries seat availability.
2. **PricingEngine**: Applies dynamic pricing rules based on time, demand, and airline quirks.
3. **PartnerNotifier**: Notifies airlines about confirmed bookings with airline-specific formatting.
4. **AuditLogger**: Writes booking activity logs to disk.
5. **BookingRepository**: Saves booking data to a proprietary database (only available in production).
6. **BookingCoordinatorImpl**: The main orchestrator that coordinates all the services.

## 📦 Prerequisites & Setup

This kata requires the **ApprovalTests** library (version 11.0.0 or later) and the **specrec** library for dependency injection.

### Virtual Environment Setup (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[test,dev]"
```

### Alternative Installation

```bash
# Install the package in development mode
pip install -e ".[test,dev]"

# Or install just the test dependencies
pip install specrec>=0.1.1 approvaltests>=11.0.0 pytest>=7.0.0
```

⚠️ **Important**: You'll need to handle test isolation and cleanup manually in Python, so consider using `pytest` fixtures for ObjectFactory clearing.

⚠️ **Decimal Precision**: This Python version uses `decimal.Decimal` for precise monetary calculations, providing exact decimal arithmetic like the Java BigDecimal version. This avoids the floating-point precision issues present in the JavaScript/TypeScript version.

### Running Tests

To run the tests:

```bash
pytest

# 🏆 Challenges

## 🥉 Inject dependencies

Did you ever run into a codebase so awkward and full of hard to override dependencies that even the thought of writing a test is daunting? When direct class instantiation liters a codebase, writing tests after the fact is a nightmare. Luckily, the `ObjectFactory` can help you out.

### 🔧 Task

Use an `ObjectFactory` pattern to write a test for `BookingCoordinatorImpl.book_flight()` that:
* Uses stubs instead of the untestable classes
* Checks that it returns the booking reference produced by the `BookingRepository`
* All *without extensive changes to the production code*.

This is **impossible** without changing the code. With an `ObjectFactory`, you can refactor the direct instantiation to use `factory.create(Class)` and inject test doubles that record behavior.

### 🏭 Concept: ObjectFactory

The `ObjectFactory` acts as a drop-in replacement for direct instantiation, allowing you to control object creation in tests.

First, import the specrec functions:
```python
from specrec import create, set_one, context
```

Instead of:
```python
logger = AuditLoggerImpl(log_directory, verbose_mode)
```

Use:
```python
logger = create(AuditLoggerImpl)(log_directory, verbose_mode)
```

Or for abstract base classes:
```python
logger: AuditLogger = create(AuditLoggerImpl)(log_directory, verbose_mode)
```

In tests, you can override what gets created using `context()` to manage test isolation:
```python
with context():
    # For concrete types
    set_one(AuditLoggerImpl, FakeAuditLogger())
    # For abstract base classes
    set_one(AuditLogger, FakeAuditLogger())
    # Return this fake once, then normal creation
    set_one(PricingEngine, FakePricingEngine())

    # Your test code here
    coordinator = BookingCoordinatorImpl()
    result = coordinator.book_flight(...)
```

#### ApprovalTests verify

When using ApprovalTests we use pytest with approval testing. ApprovalTests will compare the output against previously approved results stored in `.approved.txt` files.

Here is how you can use `set_one()` with ApprovalTests:

```python
from approvaltests import verify
from specrec import set_one, context

def test_book_flight_should_create_booking_successfully():
    with context():
        # Setup test doubles
        set_one(BookingRepositoryImpl, BookingRepositoryStub())
        # ... setup other dependencies

        coordinator = BookingCoordinatorImpl()
        result = coordinator.book_flight(passenger_name, flight_number, ...)

        verify(str(result))
```

#### Constructor arguments

If you want to test constructor arguments make sure your test double implements a method to capture constructor parameters. You can create a simple protocol for this:

```python
from typing import Protocol, Any

class ConstructorAware(Protocol):
    def constructor_called_with(self, *args: Any, **kwargs: Any) -> None:
        """Called when object is constructed with these parameters."""
        ...
```

Each parameter contains the constructor argument, allowing for better test logging and verification.

#### Singleton instance

Import and use the create function from specrec:
```python
from specrec import create

create(YourClass)(*constructor_args)
```
