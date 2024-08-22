import pytest

from cat_weather_bot.thermal_sensation import ThermalSensation


@pytest.mark.unit
def test_get_thermal_sensation():
    temperature = 5
    thermal_sensation = ThermalSensation(temperature)
    assert str(thermal_sensation) == "cold"
