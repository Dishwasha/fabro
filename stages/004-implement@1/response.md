All **55 tests pass**. Here's a summary of what was implemented:

**`tempconv/tempconv.py`** — 6 conversion functions with validation:
- `celsius_to_fahrenheit()`, `celsius_to_kelvin()`
- `fahrenheit_to_celsius()`, `fahrenheit_to_kelvin()`
- `kelvin_to_celsius()`, `kelvin_to_fahrenheit()`
- `is_valid_temperature()` — checks physical plausibility
- `TemperatureError` / `InvalidTemperatureError` — custom exceptions
- Rejects `nan`, `inf`, `-inf`, and values below absolute zero

**`tempconv/tests/test_tempconv.py`** — 55 tests covering:
- Exception hierarchy
- All 6 conversion functions at freezing/boiling/absolute-zero/zero/negative points
- Round-trip conversions (C↔F↔K in both directions)
- `is_valid_temperature()` positive and negative cases
- Parameterized `InvalidTemperatureError` raising tests
- Edge cases: sun-core temperature, large values, float return type, round-trip precision