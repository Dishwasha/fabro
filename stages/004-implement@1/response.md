All **76 tests pass**. The implementation is complete — both files were already in place:

- **`tempconv.py`** — six conversion functions (`celsius_to_fahrenheit`, `celsius_to_kelvin`, `fahrenheit_to_celsius`, `fahrenheit_to_kelvin`, `kelvin_to_celsius`, `kelvin_to_fahrenheit`) with docstrings, type hints, and input validation (`TypeError` for non-numeric, `ValueError` for negative Kelvin / NaN / Inf).
- **`test_tempconv.py`** — 76 tests across five categories: known-value conversions, absolute zero, round-trip precision, negative Kelvin, type safety, and large values.