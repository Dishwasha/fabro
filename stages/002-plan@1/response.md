All **76 tests pass**. Here's a summary of what was created:

### Files created

| File | Purpose |
|---|---|
| `plan.md` | Implementation plan with functions, edge cases, and steps |
| `tempconv.py` | Module with 6 conversion functions + input validation |
| `test_tempconv.py` | 76 pytest tests across 6 test classes |

### Module functions

- `celsius_to_fahrenheit(celsius: float) → float`
- `celsius_to_kelvin(celsius: float) → float`
- `fahrenheit_to_celsius(fahrenheit: float) → float`
- `fahrenheit_to_kelvin(fahrenheit: float) → float`
- `kelvin_to_celsius(kelvin: float) → float`
- `kelvin_to_fahrenheit(kelvin: float) → float`

### Test coverage (6 suites)

1. **TestKnownValues** — 14 tests with hand-checked reference values (freezing, boiling, body temp, etc.)
2. **TestAbsoluteZero** — 6 tests at 0 K / -273.15°C / -459.67°F
3. **TestRoundTrip** — 19 parametrized round-trip tests (convert away and back for each unit)
4. **TestNegativeKelvin** — 3 tests ensuring Kelvin < 0 raises `ValueError`
5. **TestTypeSafety** — 36 parametrized tests for `str`, `None`, `bool`, `list`, `dict` → `TypeError`, plus NaN/Inf checks
6. **TestLargeValues** — 2 tests with extreme temperatures (stellar core, solar surface)