import json
import sys

from enum import Enum
from cat_weather_bot.settings import DB_MODEL_PATH

DB_MODEL = json.loads(open(DB_MODEL_PATH, "r").read())

class ThermalSensation(Enum):
    very_cold = "very_cold"
    cold = "cold"
    chilly = "chilly"
    mild = "mild"
    hot = "hot"
    very_hot = "very_hot"

class Database:
    """
    Database class connect (or create if not exist) database json file.
    Any command executed modify attributes of class and save changes in json
    file automatic.
    """

    def __init__(self, database_filepath) -> None:
        self.database_filepath = database_filepath
        self.__data = None
        self.__connect()
        self.__generate_id_message()

    @property
    def data(self):
        return self.__data

    def __connect(self) -> None:
        """Connect database json and sync variable Database.data"""
        try:
            with open(self.database_filepath, "r") as database:
                self.__data = json.loads(database.read())
        except (json.JSONDecodeError, FileNotFoundError):
            open(self.database_filepath, "w").write(json.dumps(DB_MODEL))
            self.__data = json.loads(open(self.database_filepath, "r").read())

    def __commit(self) -> None:
        """Save Database.data in database filepath"""
        try:
            with open(self.database_filepath, "w") as database:
                retr = json.dumps(self.__data)
                database.write(retr)
        except FileNotFoundError as e:
            print(e)
            sys.exit(1)

    def __generate_id_message(self):
        """Write in dict a ID for all messages, id get list index
        reference"""
        for thermal_sensation in self.__data:
            for index, message in enumerate(self.__data[thermal_sensation]):
                if "id" in self.__data[thermal_sensation][index]:
                    self.__data[thermal_sensation][index]["id"] = index
                else:
                    self.__data[thermal_sensation][index] = {
                        "id": index,
                        **message,
                    }

    def add_thermal_sensation(self):
        """Add category thermal sensation in database"""
        pass

    def add_message_to_thermal_sensation(
        self,
        thermal_sensation: ThermalSensation,
        message: str,
        image_path: str,
    ) -> None:
        """Add message to database with a image path and run commit for save"""

        messages = [
            message["message"]
            for message in self.__data[thermal_sensation.value]
        ]
        if message in messages:
            raise ValueError("Message already exists in database")

        self.__data[thermal_sensation.value].append(
            {"message": message, "image_path": image_path}
        )
        self.__generate_id_message()
        self.__commit()

    def delete_message_to_thermal_sensation(
        self, thermal_sensation: ThermalSensation, id: int
    ):
        """Remove message to database with informer id and run
        commit for save"""
        try:
            self.__data[thermal_sensation.value].pop(id)
        except IndexError as e:
            raise IndexError(str(e))
        self.__generate_id_message()
        self.__commit()
