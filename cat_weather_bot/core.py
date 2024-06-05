import csv
import random

from cat_weather_bot.database import Database, ThermalSensation
from cat_weather_bot.utils.image import image_path_validate


class CoreFunctions:
    @staticmethod
    def read_messages(
        database: Database,
        thermal_sensation: ThermalSensation,
        id_message: int = None,
    ) -> dict:
        """
        Show messages to thermal sensation
        Case filter by id message, use parameter id_message
        """
        db = database

        try:
            if id_message == None:
                messages = db.data[thermal_sensation.value]
            else:
                messages = db.data[thermal_sensation.value][id_message]
            return messages
        except IndexError:
            print(f"Error! Id message `{id_message}` incorret")

    @staticmethod
    def read_random_message_to_thermal_sensation(
        database: Database, thermal_sensation: ThermalSensation
    ) -> dict:
        """Return message randomize by thermal sensation"""
        db = database
        messages = db.data[thermal_sensation.value]
        return random.choice(messages)

    @staticmethod
    def add_message(
        database: Database,
        thermal_sensation: ThermalSensation,
        message: str,
        image_path: str,
    ) -> None:
        """Add message to bot weather"""
        db = database

        if not image_path_validate(image_path):
            raise TypeError("Not validate image")

        db.add_message_to_thermal_sensation(
            thermal_sensation, message, image_path
        )

    @staticmethod
    def delete_message(
        database: Database,
        thermal_sensation: ThermalSensation,
        id_message: int,
    ) -> None:
        """Delete message to bot weather"""
        db = database
        db.delete_message_to_thermal_sensation(thermal_sensation, id_message)

    @staticmethod
    def import_messages(database: Database, csv_path: str) -> None:
        """Import messages for bot weather using csv file"""
        db = database

        csv_file = csv.reader(open(csv_path), delimiter="|")
        for index, line in enumerate(csv_file):
            if line[0].startswith("#"):
                continue

            thermal_sensation = line[0].strip()
            message = line[1].strip()
            image_path = line[2].strip()
            if not image_path_validate(image_path):
                raise TypeError(f"Not validate image in line {index}")

            db.add_message_to_thermal_sensation(
                ThermalSensation(thermal_sensation), message, image_path
            )
