import json
import sys
from cat_weather_bot.settings import DB_MODEL_PATH
from dataclasses import dataclass

DB_MODEL = json.loads(open(DB_MODEL_PATH, "r").read())

class Database():
    def __init__(self, database_filepath) -> None:
        self.database_filepath = database_filepath
    
    def connect(self) -> None:
        """Connect database json and create variable Database.data"""
        try:
            with open(self.database_filepath, "r") as database:
                self.data = json.loads(database.read())
        except (json.JSONDecodeError, FileNotFoundError):
                self.data = DB_MODEL


    def commit(self) -> None:
        """Save Database.data in database filepath"""
        try:
            with open(self.database_filepath, "w") as database:
                retr = json.dumps(self.data)
                database.write(retr)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)
    

    def add_temperature_category():
        pass


    def add_message_to_temperature(self, temperature: str, message: str, image_path: str) -> None:
        pass
