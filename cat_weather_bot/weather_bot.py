import logging
from dataclasses import dataclass

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from cat_weather_bot.config import GIF_HELP_COMMAND
from cat_weather_bot.models import Image, Message
from cat_weather_bot.thermal_sensation import ThermalSensation
from cat_weather_bot.weather_api import WeatherApi


@dataclass
class WeatherBot:
    """
    Comunication controller with telegram bot.

    Functions use the telegram bot for send messages and images based temperature actualy in
    location sended by user

    Need create bot in telegram api and generate token: https://core.telegram.org/bots/tutorial

    :param images: Object of class Image for defined path with images thermal sensation
    :param messages: Object of class Message for get messages used in respose
    :param weather_api: Object of class WheatherApi for consult the temperature based location
    :param telegram_token: Token generate with BotFather in telegram
    :param name: Name for used in your bot
    """

    images: Image
    messages: Message
    weather_api: WeatherApi
    telegram_token: str
    name: str = "Weather Bot"

    async def __help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = "Envie sua localização ou outra localização qualquer e aguarde a resposta"
        try:
            with open(GIF_HELP_COMMAND, "rb") as gif_file:
                await update.message.reply_document(document=gif_file, caption=message)
        except Exception as e:
            logging.error("FAILED OPEN IMAGE")
            logging.exception(e)

        return ConversationHandler.END

    async def __location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_location = update.message.location

        logging.debug(
            "Location of %s: %f / %f",
            user.first_name,
            user_location.latitude,
            user_location.longitude,
        )

        temperature_info = self.weather_api.get_temperature(
            latitude=user_location.latitude, longitude=user_location.longitude
        )

        temperature, apparent_temperature = temperature_info.values()

        thermal_sensation = ThermalSensation(temperature)

        message = self.messages.get_random_message_to_thermal_sensation(thermal_sensation)
        image = self.images.get_random_image_to_thermal_sensation(thermal_sensation)

        message_formated = message.format(
            user_first_name=user.first_name,
            temperature=temperature,
            apparent_temperature=apparent_temperature,
        )

        try:
            with open(image, "rb") as image:
                await update.message.reply_photo(photo=image, caption=message_formated)
        except Exception as e:
            logging.error("FAILED OPEN IMAGE")
            logging.exception(e)

        return ConversationHandler.END

    async def __getme(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = f"Bot Name: {self.name}, Lang: {self.weather_api.lang}"
        await update.message.reply_text(message)

    def start_bot(self):
        application = ApplicationBuilder().token(self.telegram_token).build()
        location_handler = MessageHandler(filters.LOCATION, self.__location)
        getme_handler = CommandHandler("getme", self.__getme)
        help_handler = CommandHandler("help", self.__help)
        application.add_handler(location_handler)
        application.add_handler(getme_handler)
        application.add_handler(help_handler)
        application.run_polling(allowed_updates=Update.ALL_TYPES)
