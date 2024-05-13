from dynaconf import Dynaconf
import json
import os

ROOT_PATH = os.path.dirname(__file__)
DB_PATH = os.path.join(ROOT_PATH, "assets", "database.json")
DB_MODEL_PATH = os.path.join(ROOT_PATH, "assets", "database.init.json")


dynaconf_settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    load_dotenv=True,
)

# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
