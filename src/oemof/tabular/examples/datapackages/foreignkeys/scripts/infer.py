"""
Note: This script allow does not create meta data that are valid, you will
need to set the foreign keys for the marginal_cost yourself.
"""
from oemof.tabular.datapackage import building

# This part is for testing only: It allows to pass
# the filename of inferred metadata other than the default.
if "kwargs" not in locals():
    kwargs = {}

building.infer_metadata(
    package_name="oemof-tabular-foreignkeys-examples",
    foreign_keys={
        "bus": ["component"],
        "profile": ["component"],
        "from_to_bus": [],
        "chp": [],
    },
    **kwargs,
)
