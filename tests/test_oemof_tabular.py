import oemof

from oemof.tabular import __version__


def test_version_specification():
    """ `oemof.tabular`'s version specification is importable and a string.
    """
    assert isinstance(__version__, str)
    assert isinstance(oemof.__version__, str)

