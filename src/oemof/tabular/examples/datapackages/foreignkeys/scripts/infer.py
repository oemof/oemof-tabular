"""
Note: This script allow does not create meta data that are valid, you will
need to set the foreign keys for the marginal_cost yourself.
"""

from oemof.tabular.datapackage import building

building.infer_metadata(
    package_name="oemof-tabular-foreignkeys-examples",
    foreign_keys={
        "bus": ["component"],
        "profile": ["component"],
        "from_to_bus": [],
        "chp": [],
    },
)
