Here's my analysis:

---

## Functions Needed

**6 conversion functions** (each converts one scale to another):

| Function | Formula |
|---|---|
| `celsius_to_fahrenheit(c: float) -> float` | `F = c × 9/5 + 32` |
| `celsius_to_kelvin(c: float) -> float` | `K = c + 273.15` |
| `fahrenheit_to_celsius(f: float) -> float` | `C = (f − 32) × 5/9` |
| `fahrenheit_to_kelvin(f: float) -> float` | `K = (f − 32) × 5/9 + 273.15` |
| `kelvin_to_celsius(k: float) -> float` | `C = k − 273.15` |
| `kelvin_to_fahrenheit(k: float) -> float` | `F = (k − 273.15) × 9/5 + 32` |

**2 helper functions:**
| Function | Purpose |
|---|---|
| `is_valid_temperature(value: float, scale: str) -> bool` | Check if temperature is physically possible for its scale |
| `TemperatureError` / `InvalidTemperatureError` | Custom exceptions for invalid values |

## Edge Cases

1. **Absolute zero** — 0 K = −273.15°C = −459.67°F (boundary)
2. **Below absolute zero** — negative Kelvin (must raise error)
3. **Zero values** — 0°C, 0°F, 0 K
4. **Water phase points** — freezing (0°C/32°F/273.15K) and boiling (100°C/212°F/373.15K)
5. **Negative temperatures** — valid for C/F, invalid for K
6. **Very large values** — e.g. sun core (~15.7M°C)
7. **Round-trip accuracy** — C→F→C should match within floating-point tolerance
8. **Special floats** — `inf`, `-inf`, `nan` should be rejected

The plan has been written to `plan.md` in the `tempconv/` directory. Ready to implement whenever you'd like to proceed.