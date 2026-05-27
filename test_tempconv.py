"""Tests for tempconv module."""

import pytest

import tempconv

# ── Known-value conversions ──────────────────────────────────────────────────

class TestKnownValues:
    """Conversions against hand-checked reference values."""

    def test_0c_to_fahrenheit(self):
        assert tempconv.celsius_to_fahrenheit(0) == pytest.approx(32)

    def test_100c_to_fahrenheit(self):
        assert tempconv.celsius_to_fahrenheit(100) == pytest.approx(212)

    def test_freezing_to_kelvin(self):
        assert tempconv.celsius_to_kelvin(0) == pytest.approx(273.15)

    def test_boiling_to_kelvin(self):
        assert tempconv.celsius_to_kelvin(100) == pytest.approx(373.15)

    def test_32f_to_celsius(self):
        assert tempconv.fahrenheit_to_celsius(32) == pytest.approx(0)

    def test_212f_to_celsius(self):
        assert tempconv.fahrenheit_to_celsius(212) == pytest.approx(100)

    def test_273_15k_to_celsius(self):
        assert tempconv.kelvin_to_celsius(273.15) == pytest.approx(0)

    def test_373_15k_to_celsius(self):
        assert tempconv.kelvin_to_celsius(373.15) == pytest.approx(100)

    def test_32f_to_kelvin(self):
        assert tempconv.fahrenheit_to_kelvin(32) == pytest.approx(273.15)

    def test_212f_to_kelvin(self):
        assert tempconv.fahrenheit_to_kelvin(212) == pytest.approx(373.15)

    def test_273_15k_to_fahrenheit(self):
        assert tempconv.kelvin_to_fahrenheit(273.15) == pytest.approx(32)

    def test_373_15k_to_fahrenheit(self):
        assert tempconv.kelvin_to_fahrenheit(373.15) == pytest.approx(212)

    def test_body_temperature(self):
        assert tempconv.celsius_to_fahrenheit(37) == pytest.approx(98.6)

    def test_celsius_to_kelvin_and_back(self):
        assert tempconv.kelvin_to_celsius(273.15) == pytest.approx(0)


# ── Absolute zero ────────────────────────────────────────────────────────────

class TestAbsoluteZero:
    """Conversions involving absolute zero (0 K = -273.15 °C = -459.67 °F)."""

    def test_k_to_c(self):
        assert tempconv.kelvin_to_celsius(0) == pytest.approx(-273.15)

    def test_c_to_k(self):
        assert tempconv.celsius_to_kelvin(-273.15) == pytest.approx(0)

    def test_c_to_f(self):
        assert tempconv.celsius_to_fahrenheit(-273.15) == pytest.approx(-459.67)

    def test_f_to_c(self):
        assert tempconv.fahrenheit_to_celsius(-459.67) == pytest.approx(-273.15)

    def test_f_to_k(self):
        assert tempconv.fahrenheit_to_kelvin(-459.67) == pytest.approx(0)

    def test_k_to_f(self):
        assert tempconv.kelvin_to_fahrenheit(0) == pytest.approx(-459.67)


# ── Round-trip precision ─────────────────────────────────────────────────────

class TestRoundTrip:
    """Each value converted away and back should land within tolerance."""

    @pytest.mark.parametrize(
        "value",
        [0, 20, 37, 100, -40, -273.15, 1000, 0.001],
    )
    def test_celsius_round_trip(self, value):
        f = tempconv.celsius_to_fahrenheit(value)
        assert tempconv.fahrenheit_to_celsius(f) == pytest.approx(value)

        k = tempconv.celsius_to_kelvin(value)
        assert tempconv.kelvin_to_celsius(k) == pytest.approx(value)

    @pytest.mark.parametrize(
        "value",
        [0, 32, 212, -40, 1000, 0.001],
    )
    def test_fahrenheit_round_trip(self, value):
        c = tempconv.fahrenheit_to_celsius(value)
        assert tempconv.celsius_to_fahrenheit(c) == pytest.approx(value)

        k = tempconv.fahrenheit_to_kelvin(value)
        assert tempconv.kelvin_to_fahrenheit(k) == pytest.approx(value)

    @pytest.mark.parametrize(
        "value",
        [0, 273.15, 373.15, 1000, 0.001],
    )
    def test_kelvin_round_trip(self, value):
        c = tempconv.kelvin_to_celsius(value)
        assert tempconv.celsius_to_kelvin(c) == pytest.approx(value)

        f = tempconv.kelvin_to_fahrenheit(value)
        assert tempconv.fahrenheit_to_kelvin(f) == pytest.approx(value)


# ── Negative Kelvin (ValueError) ─────────────────────────────────────────────

class TestNegativeKelvin:
    """Kelvin cannot be negative."""

    @pytest.mark.parametrize(
        "func",
        [tempconv.kelvin_to_celsius, tempconv.kelvin_to_fahrenheit],
    )
    def test_negative_raises(self, func):
        with pytest.raises(ValueError, match="kelvin must be >= 0"):
            func(-1)

    def test_zero_kelvin_is_valid(self):
        assert tempconv.kelvin_to_celsius(0) == pytest.approx(-273.15)
        assert tempconv.kelvin_to_fahrenheit(0) == pytest.approx(-459.67)


# ── Type safety ───────────────────────────────────────────────────────────────

class TestTypeSafety:
    """Non-numeric inputs should raise TypeError."""

    @pytest.mark.parametrize(
        "func",
        [
            tempconv.celsius_to_fahrenheit,
            tempconv.celsius_to_kelvin,
            tempconv.fahrenheit_to_celsius,
            tempconv.fahrenheit_to_kelvin,
            tempconv.kelvin_to_celsius,
            tempconv.kelvin_to_fahrenheit,
        ],
    )
    @pytest.mark.parametrize("bad_input", ["not a number", None, True, [25], {"c": 25}])
    def test_non_numeric_raises(self, func, bad_input):
        with pytest.raises(TypeError):
            func(bad_input)

    def test_nan_raises(self):
        with pytest.raises(ValueError):
            tempconv.celsius_to_fahrenheit(float("nan"))

    def test_inf_raises(self):
        with pytest.raises(ValueError):
            tempconv.kelvin_to_celsius(float("inf"))


# ── Large values ──────────────────────────────────────────────────────────────

class TestLargeValues:
    """Extreme temperature values."""

    def test_stellar_core(self):
        # ~15 million °C (Sun's core)
        c = 15_000_000
        f = tempconv.celsius_to_fahrenheit(c)
        k = tempconv.celsius_to_kelvin(c)
        assert f == pytest.approx(27_000_032)
        assert k == pytest.approx(15_000_273.15)

    def test_solar_surface(self):
        # ~5500 °C
        assert tempconv.celsius_to_fahrenheit(5500) == pytest.approx(9932)
        assert tempconv.celsius_to_kelvin(5500) == pytest.approx(5773.15)
