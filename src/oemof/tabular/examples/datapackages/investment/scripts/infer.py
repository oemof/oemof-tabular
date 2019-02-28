from oemof.tabular.datapackage import building

building.infer_metadata(package_name='renpass-invest-example',
                        foreign_keys={
                            'bus': ['volatile', 'dispatchable', 'storage',
                                    'load', 'shortage', 'excess', 'source'],
                            'profile': ['load', 'source'],
                            'chp': ['chp'],
                            'from_to_bus': ['link', 'conversion']
                        })
