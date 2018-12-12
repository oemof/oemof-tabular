from datapackage_utilities import building

building.infer_metadata(package_name='oemof-tabular-dispatch-example',
                        foreign_keys={
                            'bus': ['volatile', 'dispatchable', 'storage',
                                    'load'],
                            'profile': ['load', 'volatile'],
                            'from_to_bus': ['link'],
                            'chp':[]
                        })
