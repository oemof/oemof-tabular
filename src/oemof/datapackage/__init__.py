__version__ = "0.0.6dev"
__project__ = "oemof.datapackage"


import sys
import warnings

if sys.version_info[:2] == (3, 8):
    msg = (
        "You are using python version 3.8./n"
        "oemof.datapackage will stop supporting python 3.8 in the future."
    )
    warnings.warn(msg, DeprecationWarning, stacklevel=2)
