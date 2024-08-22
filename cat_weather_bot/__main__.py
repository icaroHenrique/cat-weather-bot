from cat_weather_bot.config import IMAGES_PATH, MESSAGES_FILE_PATH, settings
from cat_weather_bot.models import Image, Message
from cat_weather_bot.weather_api import WeatherApi
from cat_weather_bot.weather_bot import WeatherBot


def main():
    images = Image(IMAGES_PATH)
    messages = Message(MESSAGES_FILE_PATH)
    weather_api = WeatherApi(settings.OPEN_WEATHER_TOKEN)
    weather_bot = WeatherBot(images, messages, weather_api, settings.TELEGRAM_TOKEN)

    weather_bot.start_bot()


if __name__ == "__main__":
    main()
