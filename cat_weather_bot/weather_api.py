import logging
from dataclasses import dataclass

import requests


@dataclass
class WeatherApi:
    api_key: str
    units: str = "metric"
    mode: str = "json"
    lang: str = "pt_br"
    base_api_url: str = "https://api.openweathermap.org/data/2.5/weather"

    def __create_api_url(self):
        API_PARAMETERS = f"appid={self.api_key}&units={self.units}&mode={self.mode}&lang={self.lang}"
        API_URL = f"{self.base_api_url}?{API_PARAMETERS}"
        return API_URL

    def get_temperature(self, latitude: int, longitude: int) -> dict:
        api_url = self.__create_api_url()
        temperature_data = {}
        request = requests.get(url=f"{api_url}&lat={latitude}&lon={longitude}")
        json_request = request.json()
        logging.info(json_request)
        temperature_data["temperature"] = json_request["main"]["temp"]
        temperature_data["apparent_temperature"] = json_request["main"][
            "feels_like"
        ]
        return temperature_data
