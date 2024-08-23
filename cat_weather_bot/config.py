import logging
from os.path import dirname
from pathlib import Path

from dynaconf import Dynaconf, Validator

ROOT_PATH = Path(dirname(__file__)).resolve().parent
IMAGES_PATH = Path(ROOT_PATH, "assets/img")
MESSAGES_FILE_PATH = Path(ROOT_PATH, "assets/messages.json")
GIF_HELP_COMMAND = Path(ROOT_PATH, "assets/cat-weather-bot.gif")


settings = Dynaconf(
    envvar_prefix="CATWB",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
    validators=[
        Validator("TELEGRAM_TOKEN", must_exist=True),
        Validator("OPEN_WEATHER_TOKEN", must_exist=True),
        Validator("LOG_LEVEL", default="INFO"),
    ],
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    level=settings.LOG_LEVEL,
)
