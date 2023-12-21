import logging
from open_weather_api import OpenWeatherApi
from cat_weather_bot import CatWeatherBot
from dataclasses import dataclass
from config import settings
 
if __name__ == '__main__':
    assert settings.OPEN_WEATHER_TOKEN
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    open_weather_api = OpenWeatherApi(settings.OPEN_WEATHER_TOKEN)
    open_weather_bot = CatWeatherBot(open_weather_api, settings.TELEGRAM_TOKEN, "Cat Weather Bot")
    open_weather_bot.start_bot()