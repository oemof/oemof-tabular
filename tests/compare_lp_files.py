"""
Script to compare linear programming (LP) files for discrepancies.

This script is designed to facilitate comparison between generated LP files and
reference LP files. It utilizes the `meld` tool for visual comparison and
expects specific folder structures for the files. The script relies on
environment variables to determine the LP file names and whether multi-period
functionality should be used. It raises exceptions if required files are
missing or not found in the expected locations.

Attributes
----------
LP_FOLDER_TABULAR : pathlib.Path
    Path to the folder containing tabular LP files.
LP_FOLDER_TABULAR_MP : pathlib.Path
    Path to the folder containing multi-period tabular LP files.
LP_FOLDER_TMP : pathlib.Path
    Path to the folder for temporary LP files.
mp : bool
    Indicates whether multi-period mode is enabled. Derived from the
    environment variable MP.
lp_name : str
    The name of the LP file to compare, derived from the environment variable
    DATAPACKAGE.

Raises
------
RuntimeError
    If the DATAPACKAGE environment variable is not set.
FileNotFoundError
    If the specified LP files are not found in the expected locations.
"""

import os
import subprocess
from pathlib import Path

LP_FOLDER_TABULAR = Path(__file__).parent / "_files" / "lp_files"
LP_FOLDER_TABULAR_MP = LP_FOLDER_TABULAR / "multi-period"
LP_FOLDER_TMP = Path.home() / ".oemof" / "tmp"

mp = os.environ.get("MP", "False") == "True"

lp_name = os.environ.get("DATAPACKAGE")
if lp_name is None:
    raise RuntimeError("No DATAPACKAGE name given.")

if mp:
    tabular_file = LP_FOLDER_TABULAR_MP / f"{lp_name}_multi_period.lp"
    tmp_file = LP_FOLDER_TMP / f"{lp_name}_multi_period_tmp.lp"
else:
    tabular_file = LP_FOLDER_TABULAR / f"{lp_name}.lp"
    tmp_file = LP_FOLDER_TMP / f"{lp_name}_tmp.lp"

if not (tabular_file).exists():
    raise FileNotFoundError(
        f"Could not find {lp_name}.lp "
        f"neither in {LP_FOLDER_TABULAR} nor {LP_FOLDER_TABULAR_MP}."
    )

if not (tmp_file).exists():
    raise FileNotFoundError(
        f"Could not find {lp_name}_tmp.lp in {LP_FOLDER_TMP}."
    )

subprocess.run(["meld", str(tmp_file), str(tabular_file)])
