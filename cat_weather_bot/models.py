import json
import logging
import random
import sys
from pathlib import Path

import filetype
from cat_weather_bot.thermal_sensation import ThermalSensation


class Message:
    """
    Class responsible for reading messages from the JSON file.
    It maintains a variable with the dictionary generated by parsing the JSON file.

    JSON file need contains all thermal sensation
    """

    def __init__(self, messages_json_file: Path):
        """
        Load json file contains messages and parse in dict var.
        Validate if json file contains all thermal sensation and messages

        :param messages_json_file: json file with contains messages
        """
        try:
            with open(messages_json_file, "r") as messages_file:
                self._messages = json.loads(messages_file.read())
                self._validate_json_file(self._messages)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            logging.exception(e)
            sys.exit(1)
        except (KeyError, ValueError) as e:
            logging.error("JSON file problema:")
            logging.exception(e)
            sys.exit(1)

    def get_random_message_to_thermal_sensation(self, thermal_sensation: ThermalSensation) -> str:
        """
        Returns a message randomly filtered by thermal sensation.

        :param thermal_sensation: thermal sensation name with contains in messages
        """

        messages = self._messages[str(thermal_sensation)]

        return random.choice(messages)

    def _validate_json_file(self, dict_messages: dict):
        """
        Validate if json file contains all thermal sensation and messages

        :param dict_messages: dict with contain thermal sensation keys and messages
        """
        json_thermal_sensation = [ts for ts in dict_messages.keys()]
        all_thermal_sensations = list(ThermalSensation.get_all_thermal_sensations())

        json_thermal_sensation.sort()
        all_thermal_sensations.sort()

        if all_thermal_sensations != json_thermal_sensation:
            raise KeyError("JSON not contain all thermal sensation")
        for ts in json_thermal_sensation:
            if len(dict_messages[ts]) < 1:
                raise ValueError(f"Thermal sensation `{ts}` not contain messages")
        return True


class Image:
    """Class responsible for get images from assets."""

    def __init__(self, images_path: Path):
        """
        Validate if path contains images for all thermal sensations

        :param image_path: Path contains subfolders with thermal sensations images
        """
        try:
            if self._validate_images_path(images_path):
                self.path = images_path
        except FileNotFoundError as e:
            logging.exception(e)
            #sys.exit(1)

    def get_random_image_to_thermal_sensation(self, thermal_sensation: ThermalSensation) -> Path:
        """
        Returns a image randomly filtered by thermal sensation.

        :param thermal_sensation: thermal sensation name with contains in image
        """
        thermal_sensation_path = Path(self.path, str(thermal_sensation))
        images = [image.absolute() for image in thermal_sensation_path.iterdir()]
        image = random.choice(images)
        if self._image_validate(image):
            return image
        else:
            raise TypeError(f"Image {image} error! format not valid")

    def _image_validate(self, image_path: Path) -> bool:
        """Check image is file and if image is correct type for use"""
        return image_path.is_file() and filetype.is_image(image_path)

    def _validate_images_path(self, images_path: Path) -> bool:
        """Check images path is with correct struct"""
        dirs_in_images_path = [dir.name for dir in images_path.iterdir()]
        all_thermal_sensations = list(ThermalSensation.get_all_thermal_sensations())

        dirs_in_images_path.sort()
        all_thermal_sensations.sort()

        if all_thermal_sensations != dirs_in_images_path:
            raise FileNotFoundError("Path not contains subfolders with thermal sensations.")
        for dir in images_path.iterdir():
            if len(list(dir.iterdir())) < 1:
                raise FileNotFoundError(f"Images not found in {dir}")
        return True