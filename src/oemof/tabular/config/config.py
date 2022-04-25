
import json
import os
import pathlib

CONFIG_FOLDER = pathlib.PurePosixPath(__file__).parent

FOREIGN_KEYS_FILE = os.environ.get(
    "OEMOF_TABULAR_FOREIGN_KEYS_FILE",
    CONFIG_FOLDER / "foreign_keys.json"
)
with open(FOREIGN_KEYS_FILE, "r") as fk_file:
    FOREIGN_KEYS = json.load(fk_file)

FOREIGN_KEY_DESCRIPTORS_FILE = os.environ.get(
    "OEMOF_TABULAR_FOREIGN_KEY_DESCRIPTORS_FILE",
    CONFIG_FOLDER / "foreign_key_descriptors.json"
)
with open(FOREIGN_KEY_DESCRIPTORS_FILE, "r") as fk_descriptors_file:
    FOREIGN_KEY_DESCRIPTORS = json.load(fk_descriptors_file)
