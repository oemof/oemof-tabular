"""
Run this script from the root directory of the datapackage to update
or create meta data.
"""

from oemof.datapackage.datapackage import building

# This part is for testing only: It allows to pass
# the filename of inferred metadata other than the default.
if "kwargs" not in locals():
    kwargs = {}


building.infer_metadata(
    package_name="emission_constraint-example",
    foreign_keys={
        "bus": ["volatile", "dispatchable", "storage", "load", "excess"],
        "profile": ["load", "volatile"],
    },
    **kwargs,
)
