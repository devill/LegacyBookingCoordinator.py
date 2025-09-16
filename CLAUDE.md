# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Setup and Testing
- Install in development mode: `pip install -e .[test,dev]`
- Run tests: `pytest`
- Run tests with coverage: `pytest --cov=src/legacy_booking --cov-report=html`
- Run specific test: `pytest tests/test_module.py::test_function`

### Code Quality
- Format code: `black .`
- Type checking: `mypy .`
- Lint code: `flake8`
- Run pre-commit hooks: `pre-commit run --all-files`

## Project Overview

This is the Python version of the Legacy Booking Coordinator code kata, demonstrating how SpecRec can be used to test untestable legacy code.

### Branch Structure

- **main**: Starting position with untestable legacy code
- **bronze**: Basic ObjectFactory dependency injection
- **silver**: CallLogger integration for interaction recording
- **gold**: Full Parrot test doubles with replay
- **ruby**: Comprehensive scenario testing with data-driven tests

### Architecture

The legacy booking system coordinates:
1. **FlightAvailabilityService**: Queries seat availability
2. **PricingEngine**: Applies dynamic pricing rules
3. **PartnerNotifier**: Notifies airlines about bookings
4. **AuditLogger**: Writes booking activity logs
5. **BookingRepository**: Saves booking data
6. **BookingCoordinator**: Main orchestrator

### SpecRec Integration

Uses `specrec-python` package for:
- ObjectFactory pattern to replace direct instantiation
- Context API for test orchestration
- CallLogger for recording method interactions
- Parrot test doubles for replaying verified scenarios

### Testing Notes

- Uses pytest testing framework with approvaltests
- Tests use approval testing with `.received.txt`/`.verified.txt` files
- Each challenge branch demonstrates progressive SpecRec usage patterns
- Coverage reporting via pytest-cov
- Python 3.8+ required

### Python-Specific Patterns

- Uses type hints throughout
- Follows PEP 8 style guidelines via Black formatting
- Modern Python patterns with dataclasses and context managers
- Integration with Python's dynamic nature for transparent proxying