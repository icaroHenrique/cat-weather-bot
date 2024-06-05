import logging

from cat_weather_bot.core import CoreFunctions
from cat_weather_bot.database import Database, ThermalSensation
from cat_weather_bot.settings import DB_PATH
from cat_weather_bot.settings import dynaconf_settings as settings
from cat_weather_bot.weather_api import WeatherApi
from cat_weather_bot.weather_bot import WeatherBot

def main():
    print(settings.OPEN_WEATHER_TOKEN)
    assert settings.OPEN_WEATHER_TOKEN
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    weather_api = WeatherApi(settings.OPEN_WEATHER_TOKEN)
    database = Database(DB_PATH)
    core_functions = CoreFunctions()

    weather_bot = WeatherBot(
        ThermalSensation,
        core_functions,
        database,
        weather_api,
        settings.TELEGRAM_TOKEN,
        "Cat Weather Bot",
    )
    weather_bot.start_bot()

if __name__ == "__main__":
    main()
