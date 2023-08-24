import importlib
import importlib.resources
import os
import pathlib
import re
from difflib import unified_diff

from oemof.network.energy_system import EnergySystem as ES
from oemof.solph import helpers

# The import below is only used to monkey patch `EnergySystem`.
# Hence the `noqa` because otherwise, style checkers would complain about an
# unused import.
import oemof.tabular.datapackage  # noqa: F401
from oemof.tabular.facades import TYPEMAP

ROOT_DIR = pathlib.Path(__file__).parent.parent


def chop_trailing_whitespace(lines):
    return [re.sub(r"\s*$", "", line) for line in lines]


def remove(pattern, lines):
    if not pattern:
        return lines
    return re.subn(pattern, "", "\n".join(lines))[0].split("\n")


def compare_json_files(file_1, file_2, ignored=None):
    lines_1 = remove(ignored, chop_trailing_whitespace(file_1.readlines()))
    lines_2 = remove(ignored, chop_trailing_whitespace(file_2.readlines()))

    if not lines_1 == lines_2:
        raise AssertionError(
            "Failed matching json_file_1 with json_file_2:\n"
            + "\n".join(
                unified_diff(
                    lines_1,
                    lines_2,
                    fromfile=os.path.relpath(file_1.name),
                    tofile=os.path.basename(file_2.name),
                    lineterm="",
                )
            )
        )


def test_example_datapackage_readability():
    """The example datapackages can be read and loaded."""

    systems = []
    datapackage_dir = os.path.join(
        importlib.resources.files("oemof.tabular"), "examples/datapackages"
    )
    for example in os.listdir(datapackage_dir):
        print("Runnig reading datapackage example {} ...".format(example))
        systems.append(
            ES.from_datapackage(
                os.path.join(datapackage_dir, example, "datapackage.json"),
                typemap=TYPEMAP,
            )
        )

    for system in systems:
        assert type(system) is ES


def test_scripting_examples():
    """ """

    exclude = ["plotting.py", "__pycache__"]
    examples_dir = os.path.join(
        importlib.resources.files("oemof.tabular"), "examples/scripting"
    )
    for example in os.listdir(examples_dir):
        if not example.endswith(".ipynb") and example not in exclude:
            print("Running scripting example {} ...".format(example))
            exec(open(os.path.join(examples_dir, example)).read())


def test_examples_datapackages_scripts_infer():
    """ """
    script = "infer.py"

    import pkg_resources as pkg

    for example_datapackage in pkg.resource_listdir(
        "oemof.tabular", "examples/datapackages/"
    ):
        script_path = (
            ROOT_DIR
            / "src"
            / "oemof"
            / "tabular"
            / "examples"
            / "datapackages"
            / example_datapackage
            / "scripts"
            / script
        )
        datapackage_path = (
            ROOT_DIR
            / "src"
            / "oemof"
            / "tabular"
            / "examples"
            / "datapackages"
            / example_datapackage
        )
        if script_path.exists():
            print(
                "Running infer script for {} ...".format(example_datapackage)
            )
            exec(
                "kwargs = {} \n"
                f"kwargs['path'] = '{datapackage_path}' \n"
                f"kwargs['metadata_filename'] = "
                f"'datapackage_{example_datapackage}.json' \n"
                + open(script_path).read(),
            )

            # Move metadata string to .oemof directory
            test_filepath = (
                datapackage_path / f"datapackage_{example_datapackage}.json"
            )
            new_filepath = (
                pathlib.PosixPath(helpers.extend_basic_path("metadata"))
                / f"datapackage_{example_datapackage}.json"
            )
            os.rename(test_filepath, new_filepath)

            ref_filepath = datapackage_path / "datapackage.json"

            with open(new_filepath) as new_file:
                with open(ref_filepath) as ref_file:
                    compare_json_files(new_file, ref_file)


def test_custom_foreign_keys(monkeypatch):
    """
    Set custom foreign keys
    """
    monkeypatch.setenv(
        "OEMOF_TABULAR_FOREIGN_KEY_DESCRIPTORS_FILE",
        ROOT_DIR / "tests" / "custom_foreign_key_descriptors.json",
    )
    monkeypatch.setenv(
        "OEMOF_TABULAR_FOREIGN_KEYS_FILE",
        ROOT_DIR / "tests" / "custom_foreign_keys.json",
    )
    importlib.reload(oemof.tabular.config.config)
    oemof.tabular.datapackage.building.infer_metadata(
        path=str(
            ROOT_DIR
            / "src"
            / "oemof"
            / "tabular"
            / "examples"
            / "datapackages"
            / "foreignkeys"
        ),
        package_name="oemof-tabular-foreignkeys-examples",
    )
