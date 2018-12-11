from datapackage_utilities import building

building.infer_metadata(package_name='renpass-invest-example',
                        foreign_keys={
                            'bus': ['volatile', 'dispatchable', 'storage',
                                    'load', 'shortage', 'excess', 'source'],
                            'profile': ['load', 'volatile', 'source'],
                            'chp': ['backpressure', 'extraction', 'chp'],
                            'from_to_bus': ['connection', 'line', 'conversion']
                        })
