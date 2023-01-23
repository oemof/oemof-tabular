import pytest

import oemof.tabular.datapackage.building as otdb


def test_how_initialize_loads_the_default_configuration():
    """Test how `initialize` handles a `False`y first argument.

    If `initialize <oemof.tabular.datapackage.building.initialize>` is
    called with a first argument that evaluates to `False` when
    converted to boolean it should try to load the default
    configuration. This test makes sure that this is happening, by
    checking that calling `initialize` with a `False`y first argument
    raises a `FileNotFoundError`, which happens because the test
    environment doesn't contain a default configuration, and that the
    error message contains the name of the default configuration.

    The regression that this guards against is that the wrong function
    was used to load the default configuration because the function was
    renamed at it's use in `initialize` didn't get updated to the new
    name.
    """
    with pytest.raises(FileNotFoundError) as error_info:
        otdb.initialize(config=False)
    default = "config.json"
    errormessage = str(error_info.value)
    assert default in errormessage, (
        "default '{}' not found in error message:\n{}"
    ).format(default, errormessage)
