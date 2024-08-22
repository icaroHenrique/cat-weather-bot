import pytest
from unittest.mock import Mock, patch

from cat_weather_bot.weather_api import WeatherApi

@pytest.mark.unit
@patch('cat_weather_bot.weather_api.requests.get')
def test_request_api_mock(mock_get):
    mock = {
        "main": {
            "temp": 15,
            "feels_like": 16
        }
    }
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.json.return_value = mock

    api = WeatherApi("teste")
    response = api.get_temperature(12, 13)

    print(response)
    for key in response.keys():
        assert key == "temperature" or key == "apparent_temperature"

