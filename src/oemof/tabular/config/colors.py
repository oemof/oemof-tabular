import pathlib
import json

CONFIG_FOLDER = pathlib.PurePath(__file__).parent

with open(CONFIG_FOLDER / "colors" / "TECH_COLOR_MAP.json", "r") as file:
    TECH_COLOR_MAP = json.load(file)

with open(CONFIG_FOLDER / "colors" / "CARRIER_COLOR_MAP.json", "r") as file:
    CARRIER_COLOR_MAP = json.load(file)
