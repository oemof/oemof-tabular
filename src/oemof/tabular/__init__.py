__version__ = "0.0.4dev"
__project__ = "oemof.tabular"


import sys
import warnings

major, minor, micro = sys.version_info[:3]
if minor < 9:
    warnings.warn(
        f"You are using python version {major}.{minor}.{micro}. oemof.tabular "
        "will stop supporting python < 3.9 in the future."
    )
