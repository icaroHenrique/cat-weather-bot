import logging
from dataclasses import dataclass

import requests
from requests import HTTPError


@dataclass
class WeatherApi:
    """
    Class responsability comunication API for get temperature with location informer
    Is used Open Wheter Map with request temperatures

    Documentation: https://openweathermap.org/current

    :param api_key: API KEY for authentication in Open Wheter Map
    :param units: Units used in consult temperature. Metric return value in Celsius and imperial
    return value in Fahrenheit.
    :param lang: parameter to get the output in language specify.
    """

    api_key: str
    units: str = "metric"
    lang: str = "pt_br"

    base_api_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_temperature(self, latitude: int, longitude: int) -> dict:
        """Return temperature based latitude and longitude parameters"""
        api_url = self.__create_api_url()
        temperature_data = {}

        try:
            request = requests.get(url=f"{api_url}&lat={latitude}&lon={longitude}")
        except HTTPError as e:
            logging.error("Request weather api failed")
            logging.exception(e)
        else:
            json_request = request.json()

            logging.debug(json_request)

            temperature_data["temperature"] = json_request["main"]["temp"]
            temperature_data["apparent_temperature"] = json_request["main"]["feels_like"]
            return temperature_data

    def __create_api_url(self):
        api_parameters = f"appid={self.api_key}&units={self.units}\
        &mode=json&lang={self.lang}".replace(
            " ", ""
        )
        api_url = f"{self.base_api_url}?{api_parameters}"
        return api_url
