import oemof.solph

import oemof.datapackage


def test_version_specification():
    """`
    oemof.datapackage`'s version specification is importable and a string.
    """
    assert isinstance(oemof.datapackage.__version__, str)
    assert isinstance(oemof.solph.__version__, str)


def test_project_name():
    """`oemof.datapackage`'s project name is importable and correct."""
    assert oemof.datapackage.__project__ == "oemof.datapackage"
