from pathlib import Path

import pytest

from cat_weather_bot.config import IMAGES_PATH
from cat_weather_bot.models import Image
from cat_weather_bot.thermal_sensation import ThermalSensation


@pytest.mark.unit
def test_get_path_image_all_thermal_sensation():
    images = Image(IMAGES_PATH)
    for ts in ThermalSensation.get_all_thermal_sensations():
        assert isinstance(images.get_random_image_to_thermal_sensation(ts), Path)


@pytest.mark.unit
def test_negative_image_path():
    with pytest.raises(FileNotFoundError) as error:
        images = Image(Path(IMAGES_PATH))
        images._validate_images_path(Path())
    assert str(error.value) == "Path not contains subfolders with thermal sensations."


@pytest.mark.unit
def test_open_image_get_random_image():
    images = Image(IMAGES_PATH)
    for ts in ThermalSensation.get_all_thermal_sensations():
        image = images.get_random_image_to_thermal_sensation(ts)
        try:
            with open(image, "rb"):
                validate_image = True
        except Exception:
            validate_image = False

        assert validate_image
