"""Temperature conversion utilities between Celsius, Fahrenheit, and Kelvin."""

from __future__ import annotations


def _validate_number(value: float, name: str) -> None:
    """Raise TypeError if *value* is not a number, and ValueError if it is NaN/Inf."""
    if isinstance(value, bool):
        raise TypeError(f"{name} must be a number, got bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number, got {type(value).__name__}")
    if value != value:  # NaN check
        raise ValueError(f"{name} must not be NaN")
    if value == float("inf") or value == float("-inf"):
        raise ValueError(f"{name} must not be infinite")


def celsius_to_fahrenheit(celsius: float) -> float:
    """Convert Celsius to Fahrenheit.

    Formula:  °F = °C × 9/5 + 32
    """
    _validate_number(celsius, "celsius")
    return celsius * 9 / 5 + 32


def celsius_to_kelvin(celsius: float) -> float:
    """Convert Celsius to Kelvin.

    Formula:  K = °C + 273.15
    """
    _validate_number(celsius, "celsius")
    return celsius + 273.15


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Convert Fahrenheit to Celsius.

    Formula:  °C = (°F − 32) × 5/9
    """
    _validate_number(fahrenheit, "fahrenheit")
    return (fahrenheit - 32) * 5 / 9


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Convert Fahrenheit to Kelvin.

    Formula:  K = (°F − 32) × 5/9 + 273.15
    """
    _validate_number(fahrenheit, "fahrenheit")
    return (fahrenheit - 32) * 5 / 9 + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Convert Kelvin to Celsius.

    Raises ValueError if *kelvin* is below absolute zero.

    Formula:  °C = K − 273.15
    """
    _validate_number(kelvin, "kelvin")
    if kelvin < 0:
        raise ValueError(f"Temperature in kelvin must be >= 0, got {kelvin}")
    return kelvin - 273.15


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Convert Kelvin to Fahrenheit.

    Raises ValueError if *kelvin* is below absolute zero.

    Formula:  °F = (K − 273.15) × 9/5 + 32
    """
    _validate_number(kelvin, "kelvin")
    if kelvin < 0:
        raise ValueError(f"Temperature in kelvin must be >= 0, got {kelvin}")
    return (kelvin - 273.15) * 9 / 5 + 32
