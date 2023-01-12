__config_version__ = 1

GLOBALS = {
    "serializer": "{{major}}.{{minor}}.{{patch}}{{status if status}}",
}

FILES = [
    {"path": "README.rst", "serializer": "{{major}}.{{minor}}.{{patch}}"},
    "docs/conf.py",
    "setup.py",
    "src/oemof/tabular/__init__.py",
]

VERSION = [
    "major",
    "minor",
    "patch",
    {"name": "status", "type": "value_list", "allowed_values": ["", "dev"]},
]
