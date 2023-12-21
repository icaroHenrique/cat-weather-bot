import logging
import os
import random
from dataclasses import dataclass
from open_weather_api import OpenWeatherApi
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler

@dataclass
class CatWeatherBot():
    open_weather_api: OpenWeatherApi
    telegram_token: str
    name: str = "Weather Bot"

    def __define_temperature_representation(self, temperature: int | float):
        temperature_representation = str()
        
        if temperature < 0:
            temperature_representation = "very_cold"
        elif temperature > 0 and temperature < 10:
            temperature_representation = "cold"
        elif temperature > 10 and temperature < 15:
            temperature_representation = "chilly"
        elif temperature > 15 and temperature < 25:
            temperature_representation = "mild"
        elif temperature > 25 and temperature < 35:
            temperature_representation = "hot"
        elif temperature > 35:
            temperature_representation = "very_hot"
        
        return temperature_representation

    def __get_random_image_showing_temperature(self, temperature: int | float) -> str:
        path_images = f"{os.path.dirname(os.path.abspath(__file__))}/inc/img"
        print(temperature)
        temperature_representation = self.__define_temperature_representation(temperature)

        list_files_img_dir = os.listdir(f"{path_images}/{temperature_representation}/")
        randomize_image = random.choice(list_files_img_dir)

        return f"{path_images}/{temperature_representation}/{randomize_image}"
    
    def __get_random_text_showing_temperature(self, temperature: int | float) -> str:
        path_texts = f"{os.path.dirname(os.path.abspath(__file__))}/inc/txt"
        temperature_representation = self.__define_temperature_representation(temperature)
        get_file_txt = f"{path_texts}/{temperature_representation}.txt"

        with open(get_file_txt, 'r') as file:
            lines = file.readlines()
            random_line = random.choice(lines)
            random_line = random_line.replace('\\n', '\n') #fix bug with \n in texts files
        
        return random_line

    async def __location(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.message.from_user
        user_location = update.message.location
        
        logging.info(
            "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
        )
        
        temperature_info = self.open_weather_api.get_temperature(latitude=user_location.latitude, longitude=user_location.longitude)
        temperature = temperature_info['temperature']
        apparent_temperature = temperature_info['apparent_temperature']

        random_image = self.__get_random_image_showing_temperature(apparent_temperature)
        random_text = self.__get_random_text_showing_temperature(apparent_temperature)

        text_formated = random_text.format(user_first_name=user.first_name, temperature=temperature, apparent_temperature=apparent_temperature)
        image = open(random_image, "rb")
        
        await update.message.reply_photo(photo=image, caption=text_formated)
        
        image.close()
        return ConversationHandler.END 

    async def __getme(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

