import logging
from dataclasses import dataclass

from cat_weather_bot.core import CoreFunctions
from cat_weather_bot.database import Database, ThermalSensation
from cat_weather_bot.weather_api import WeatherApi
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

@dataclass
class WeatherBot:
    thermal_sensation: ThermalSensation
    core: CoreFunctions
    database: Database
    weather_api: WeatherApi
    telegram_token: str
    name: str = "Weather Bot"

    def __define_thermal_sensation(self, temperature: int | float):
        thermal_sensations_check = {
            "very_cold": lambda temperature: temperature < 0,
            "cold": lambda temperature: temperature > 0 and temperature <= 10,
            "chilly": lambda temperature: temperature > 10
            and temperature <= 15,
            "mild": lambda temperature: temperature > 15 and temperature <= 25,
            "hot": lambda temperature: temperature > 25 and temperature <= 35,
            "very_hot": lambda temperature: temperature > 35,
        }

        for (
            thermal_sensation,
            thermal_sensation_check,
        ) in thermal_sensations_check.items():
            if thermal_sensation_check(temperature):
                thermal_sensation_define = thermal_sensation

        return ThermalSensation(thermal_sensation_define)

    async def __location(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        user = update.message.from_user
        user_location = update.message.location

        logging.info(
            "Location of %s: %f / %f",
            user.first_name,
            user_location.latitude,
            user_location.longitude,
        )

        temperature_info = self.weather_api.get_temperature(
            latitude=user_location.latitude, longitude=user_location.longitude
        )

        temperature, apparent_temperature = temperature_info.values()

        thermal_sensation = self.__define_thermal_sensation(temperature)

        message = self.core.read_random_message_to_thermal_sensation(
            self.database, thermal_sensation
        )

        image_path = message["image_path"]
        text = message["message"]

        text_formated = text.format(
            user_first_name=user.first_name,
            temperature=temperature,
            apparent_temperature=apparent_temperature,
        )
        image = open(image_path, "rb")

        await update.message.reply_photo(photo=image, caption=text_formated)

        image.close()
        return ConversationHandler.END

    async def __getme(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        bot = update.get_bot()
        message = update.message.to_json()
        print(message)
        print(await bot.get_me())

    def start_bot(self):
        application = ApplicationBuilder().token(self.telegram_token).build()
        location_handler = MessageHandler(filters.LOCATION, self.__location)
        getme_handler = CommandHandler("getme", self.__getme)
        application.add_handler(location_handler)
        application.add_handler(getme_handler)
        application.run_polling(allowed_updates=Update.ALL_TYPES)
