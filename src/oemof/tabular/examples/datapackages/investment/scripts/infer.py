from oemof.tabular.datapackage import building


# This part is for testing only: It allows to pass
# the filename of inferred metadata other than the default.
if not "kwargs" in locals():
    kwargs = {}

building.infer_metadata(
    package_name="renpass-invest-example",
    foreign_keys={
        "bus": [
            "volatile",
            "dispatchable",
            "storage",
            "load",
            "shortage",
            "excess",
            "source",
        ],
        "profile": ["load", "source"],
        "chp": ["chp"],
        "from_to_bus": ["link", "conversion"],
    },
    **kwargs,
)
