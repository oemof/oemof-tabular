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
    package_name="GHG-test",
    foreign_keys={
        "bus": ["commodity_ghg", "load", "excess", "gas_import"],
        "profile": ["load"],
        "from_bus": ["conversion_ghg"],
        "to_bus": ["conversion_ghg"],
        "emission_bus_0": ["conversion_ghg", "commodity_ghg"],
        "emission_bus_1": ["conversion_ghg"],
        "emission_bus_2": ["conversion_ghg"],
    },
    **kwargs,
)
