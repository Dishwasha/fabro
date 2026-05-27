# Plan: Temperature Conversion Module (tempconv.py)

## Overview
Create a Python module that converts between Celsius, Fahrenheit, and Kelvin with proper validation and pytest tests.

## Functions & Signatures

### Core conversions (3 base functions — each converts *from* one scale *to* the other two)

| Function | Signature | Description |
|---|---|---|
| `celsius_to_fahrenheit(c: float) -> float` | `c: float` → `float` | Celsius → Fahrenheit: `F = c * 9/5 + 32` |
| `celsius_to_kelvin(c: float) -> float` | `c: float` → `float` | Celsius → Kelvin: `K = c + 273.15` |
| `kelvin_to_celsius(k: float) -> float` | `k: float` → `float` | Kelvin → Celsius: `C = k - 273.15` |
| `fahrenheit_to_celsius(f: float) -> float` | `f: float` → `float` | Fahrenheit → Celsius: `C = (f - 32) * 5/9` |
| `fahrenheit_to_kelvin(f: float) -> float` | `f: float` → `float` | Fahrenheit → Kelvin: `K = (f - 32) * 5/9 + 273.15` |
| `kelvin_to_fahrenheit(k: float) -> float` | `k: float` → `float` | Kelvin → Fahrenheit: `F = (k - 273.15) * 9/5 + 32` |

### Convenience / reverse helpers

| Function | Signature | Description |
|---|---|---|
| `fahrenheit_to_kelvin(f: float) -> float` | `f: float` → `float` | Direct F→K |
| `kelvin_to_fahrenheit(k: float) -> float` | `k: float` → `float` | Direct K→F |

### Validation

| Function | Signature | Description |
|---|---|---|
| `is_valid_temperature(value: float, scale: str) -> bool` | `value: float`, `scale: str` → `bool` | Returns `True` if temperature is physically possible for the given scale (e.g. Kelvin ≥ 0) |

### Custom exceptions

| Exception | When raised |
|---|---|
| `TemperatureError` | Base exception for temperature-related errors |
| `InvalidTemperatureError` | Value below absolute zero for the given scale |

## Edge Cases to Test

1. **Absolute zero** — 0 K = -273.15°C = -459.67°F (boundary)
2. **Below absolute zero** — negative Kelvin, Kelvin values below -273.15°C (must raise error or return False)
3. **Zero values** — 0°C, 0°F, 0 K
4. **Water freezing / boiling points** — 0°C/32°F/273.15K, 100°C/212°F/373.15K
5. **Negative temperatures** — valid for Celsius/Fahrenheit, invalid for Kelvin
6. **Very large temperatures** — e.g. sun core ~15,700,000°C
7. **Round-trip conversions** — C→F→C should return the original value (within floating-point tolerance)
8. **Special float values** — `inf`, `-inf`, `nan` (should raise errors or be rejected)
9. **Precision** — results rounded to a reasonable number of decimal places

## Implementation Order

1. Create `tempconv.py` with custom exception classes
2. Implement the 6 conversion functions with validation
3. Add `is_valid_temperature()` helper
4. Create `tests/test_tempconv.py` with comprehensive pytest cases

## File Structure

```
tempconv/
├── plan.md
├── tempconv.py
└── tests/
    └── test_tempconv.py
```
