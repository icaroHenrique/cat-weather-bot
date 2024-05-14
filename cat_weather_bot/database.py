import json
import sys

from settings import DB_MODEL_PATH, DB_PATH

DB_MODEL = json.loads(open(DB_MODEL_PATH, "r").read())


class Database:
    def __init__(self, database_filepath) -> None:
        self.database_filepath = database_filepath
        self.__connect()

    @property
    def data(self):
        return self.__data

    def __connect(self) -> None:
        """Connect database json and sync variable Database.data"""
        try:
            with open(self.database_filepath, "r") as database:
                self.__data = json.loads(database.read())
        except (json.JSONDecodeError, FileNotFoundError):
            self.__data = DB_MODEL

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
        """Write in dict a ID for all messages, id get list index reference"""
        for temperature in self.__data:
            for index, message in enumerate(self.__data[temperature]):
                if "id" in self.__data[temperature][index]:
                    self.__data[temperature][index]["id"] = index
                else:
                    self.__data[temperature][index] = {"id": index, **message}

    def add_temperature():
        pass

    def add_message_to_temperature(
        self, temperature: str, message: str, image_path: str
    ) -> None:
        """Add message to database with a image path and run commit for save"""
        self.__data[temperature].append(
            {"message": message, "image_path": image_path}
        )
        self.__generate_id_message()
        self.__commit()

    def delete_message_to_temperature(self, temperature: str, id: int):
        """Remove message to database with informer id and run commit for save"""
        try:
            self.__data[temperature].pop(id)
        except IndexError as e:
            print(e)
        self.__generate_id_message()
        self.__commit()
