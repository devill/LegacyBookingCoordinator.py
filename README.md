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

Instead of:
```python
logger = AuditLoggerImpl(log_directory, verbose_mode)
```

Use:
```python
logger = factory.create(AuditLoggerImpl, log_directory, verbose_mode)
```

Or for abstract base classes:
```python
logger: AuditLogger = factory.create(AuditLoggerImpl, log_directory, verbose_mode)
```

In tests, you can override what gets created:
```python
# For concrete types
factory.set_always(AuditLoggerImpl, FakeAuditLogger())
# For abstract base classes
factory.set_always(AuditLogger, FakeAuditLogger())
# Return this fake once, then normal creation
factory.set_one(PricingEngine, FakePricingEngine())
```

#### ApprovalTests verify

When using ApprovalTests we use pytest with approval testing. ApprovalTests will compare the output against previously approved results stored in `.approved.txt` files.

Here is how you can call `factory.set_one()` using ApprovalTests:

```python
from approvaltests import verify

def test_book_flight_should_create_booking_successfully():
    # Setup test doubles
    factory.set_one(BookingRepositoryImpl, BookingRepositoryStub())
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

You can either inject an instance of the factory (harder, but better long term) or use the Singleton instance:
```python
ObjectFactory.get_instance().create(YourClass, *constructor_args)
```

Or use a module-level factory for cleaner syntax:
```python
from object_factory import create

create(YourClass, *constructor_args)
```

## 📦 Prerequisites

This kata requires the **ApprovalTests** library (version 11.0.0 or later) which provides approval testing utilities for Python.

### Installation

```bash
# Install the package in development mode
pip install -e ".[test,dev]"

# Or install just the test dependencies
pip install approvaltests>=11.0.0 pytest>=7.0.0
```

### Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[test,dev]"
```

⚠️ **Important**: You'll need to handle test isolation and cleanup manually in Python, so consider using `pytest` fixtures for ObjectFactory clearing.

⚠️ **Decimal Precision**: This Python version uses `decimal.Decimal` for precise monetary calculations, providing exact decimal arithmetic like the Java BigDecimal version. This avoids the floating-point precision issues present in the JavaScript/TypeScript version.

## 🚀 Running the Tests

To run the tests:

```bash
pytest
```

To run tests with coverage:

```bash
pytest --cov=src/legacy_booking
```

To run a specific test:

```bash
pytest tests/test_booking_coordinator.py::TestBookingCoordinator::test_book_flight_should_create_booking_successfully
```

To run tests in verbose mode:

```bash
pytest -v
```

To run tests with approval test auto-approval (be careful!):

```bash
pytest --approvaltests-use-reporter=PythonNativeReporter
```

## 🔧 Development Setup

### Code Quality Tools

This project includes modern Python development tools:

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
black src/ tests/ && flake8 src/ tests/ && mypy src/ && pytest
```

### Package Management

The project uses modern Python packaging with `pyproject.toml`:

```bash
# Install in development mode
pip install -e ".[test,dev]"

# Build distribution
pip install build
python -m build
```

## 🐍 Python-Specific Notes

### Type Hints
This codebase uses Python type hints throughout while maintaining the intentionally bad business logic. The typing helps with IDE support and catching some errors, but doesn't fix the underlying design issues.

### Decimal Precision
Unlike the JavaScript/TypeScript version, this Python implementation uses `decimal.Decimal` for all monetary calculations, providing exact decimal arithmetic without floating-point precision issues.

### Snake Case
Python conventions use `snake_case` for method and variable names (converted from the original C# `camelCase`), but the terrible design patterns remain intact.

### Abstract Base Classes
Python's `abc` module provides the equivalent of interfaces, using `@abstractmethod` decorators to define contracts that must be implemented.