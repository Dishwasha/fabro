# Plan: Temperature Conversion Module (tempconv.py)

## Goal
Create a Python module (`tempconv.py`) that converts between Celsius, Fahrenheit, and Kelvin, with corresponding `pytest` tests.

## Functions

| # | Function | Signature | Description |
|---|---|---|---|
| 1 | `celsius_to_fahrenheit` | `(celsius: float) -> float` | °C → °F |
| 2 | `celsius_to_kelvin` | `(celsius: float) -> float` | °C → K |
| 3 | `fahrenheit_to_celsius` | `(fahrenheit: float) -> float` | °F → °C |
| 4 | `fahrenheit_to_kelvin` | `(fahrenheit: float) -> float` | °F → K |
| 5 | `kelvin_to_celsius` | `(kelvin: float) -> float` | K → °C |
| 6 | `kelvin_to_fahrenheit` | `(kelvin: float) -> float` | K → °F |

## Edge Cases

1. **Absolute zero** — 0 K = -273.15 °C = -459.67 °F; conversions must produce exact equivalents.
2. **Negative Kelvin** — physically impossible; raise `ValueError`.
3. **Zero values** — 0 °C (water freezes), 0 °F, 0 K (absolute zero).
4. **Large values** — extreme temperatures (e.g., 10 000 °C).
5. **Floating-point precision** — round-trip conversions (e.g., °C → °F → °C) must stay within tolerance.
6. **Type safety** — non-numeric inputs (`str`, `None`, etc.) should raise `TypeError`.

## Implementation Steps

1. **Create `tempconv.py`** with all six conversion functions, docstrings, and type hints. Add input validation (negative Kelvin → `ValueError`, non-numeric → `TypeError`).
2. **Create `test_tempconv.py`** with pytest tests covering:
   - Known-value conversions (e.g., 0 °C = 32 °F, 100 °C = 212 °F, 0 °C = 273.15 K).
   - Round-trip precision (each value converted away and back, asserted within `pytest.approx`).
   - Absolute zero conversions in both directions.
   - Negative Kelvin raising `ValueError`.
   - Non-numeric inputs raising `TypeError`.
   - Large values.
3. **Run pytest** to verify all tests pass.
