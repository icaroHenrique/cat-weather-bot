import os

import filetype


def image_path_validate(image_path: str) -> bool:
    return os.path.isfile(image_path) and filetype.is_image(image_path)
