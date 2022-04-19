import pathlib

import pkg_resources as pkg

from oemof.network.energy_system import EnergySystem as ES

from oemof.tabular.facades import TYPEMAP

# The import below is only used to monkey patch `EnergySystem`.
# Hence the `noqa` because otherwise, style checkers would complain about an
# unused import.
import oemof.tabular.datapackage  # noqa: F401

ROOT_DIR = pathlib.Path(__file__).parent.parent


def test_example_datapackage_readability():
    """ The example datapackages can be read and loaded.
    """

    systems = []
    for example in pkg.resource_listdir(
        "oemof.tabular", "examples/datapackages"
    ):

        print("Runnig reading datapackage example {} ...".format(example))
        systems.append(
            ES.from_datapackage(
                pkg.resource_filename(
                    "oemof.tabular",
                    "examples/datapackages/{}/datapackage.json".format(
                        example
                    ),
                ),
                typemap=TYPEMAP,
            )
        )

    for system in systems:
        assert type(system) is ES


def test_scripting_examples():
    """
    """

    exclude = ["plotting.py", "__pycache__"]
    for example in pkg.resource_listdir("oemof.tabular", "examples/scripting"):
        if not example.endswith(".ipynb") and example not in exclude:
            print("Runnig scripting example {} ...".format(example))
            exec(
                open(
                    pkg.resource_filename(
                        "oemof.tabular",
                        "examples/scripting/{}".format(example),
                    )
                ).read()
            )


def test_custom_foreign_keys(monkeypatch):
    """
    Set custom foreign keys
    """
    monkeypatch.setenv(
        "OEMOF_TABULAR_FOREIGN_KEY_DESCRIPTORS_FILE",
        ROOT_DIR / "tests" / "custom_foreign_key_descriptors.json"
    )
    monkeypatch.setenv(
        "OEMOF_TABULAR_FOREIGN_KEYS_FILE",
        ROOT_DIR / "tests" / "custom_foreign_keys.json"
    )
    import importlib
    importlib.reload(oemof.tabular.config.config)
    oemof.tabular.datapackage.building.infer_metadata(
        path=str(
            ROOT_DIR / "src" / "oemof" / "tabular" / "examples" /
            "datapackages" / "foreignkeys"
        ),
        package_name="oemof-tabular-foreignkeys-examples",
    )
