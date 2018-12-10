import oemof

import oemof.tabular


def test_version_specification():
    """ `oemof.tabular`'s version specification is importable and a string.
    """
    assert isinstance(oemof.tabular.__version__, str)
    assert isinstance(oemof.__version__, str)

