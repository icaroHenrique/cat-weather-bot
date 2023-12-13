import logging
from open_weather_api import OpenWeatherApi
from cat_weather_bot import CatWeatherBot
from dataclasses import dataclass
from global_variables import TELEGRAM_TOKEN, OPEN_WEATHER_TOKEN

if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    open_weather_api = OpenWeatherApi(OPEN_WEATHER_TOKEN)
    open_weather_bot = CatWeatherBot(open_weather_api, TELEGRAM_TOKEN, "Cat Weather Bot")
    open_weather_bot.start_bot()