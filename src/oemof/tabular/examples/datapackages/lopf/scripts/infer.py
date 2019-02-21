from datapackage_utilities import building

building.infer_metadata(
    package_name='oemof-tabular-lopf-example',
    foreign_keys={
        'bus': ['volatile', 'dispatchable', 'load'],
        'profile': [],
        'from_to_bus': ['line'],
        'chp': [],
    },
)
