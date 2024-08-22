import pytest

from cat_weather_bot.config import MESSAGES_FILE_PATH
from cat_weather_bot.models import Message
from cat_weather_bot.thermal_sensation import ThermalSensation

@pytest.mark.unit
def test_get_messages_all_thermal_sensation():
    messages = Message(MESSAGES_FILE_PATH)
    for ts in ThermalSensation.get_all_thermal_sensations():
        assert isinstance(messages.get_random_message_to_thermal_sensation(ts), str)
