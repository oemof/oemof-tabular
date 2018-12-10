import oemof

import oemof.tabular


def test_version_specification():
    """ `oemof.tabular`'s version specification is importable and a string.
    """
    assert isinstance(oemof.tabular.__version__, str)
    assert isinstance(oemof.__version__, str)

def test_project_name():
    """ `oemof.tabular`'s project name is importable and correct.
    """
    assert (oemof.tabular.__project__ == 'oemof.tabular')

