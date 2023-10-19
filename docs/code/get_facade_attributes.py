import dataclasses
import os

import pandas as pd


def get_facade_attrs(TYPEMAP):
    facade_attrs = {}
    for key, facade in TYPEMAP.items():
        if dataclasses.is_dataclass(facade):
            cls_name = facade.__name__
            fields = dataclasses.fields(facade)
            df = pd.DataFrame.from_dict(
                {
                    "name": [field.name for field in fields],
                    "type": [field.type.__name__ if hasattr(field.type, "__name__") else field.type for field in fields ],
                    "default": [None if isinstance(field.default, dataclasses._MISSING_TYPE) else field.default for field in fields],
                },
            )
            df = df.set_index("name")

            facade_attrs[cls_name] = df

    return facade_attrs


def write_table_rst(csv_directory, destination):
    csv_files = sorted([file for file in os.listdir(csv_directory) if file.endswith(".csv")])
    txt = ""
    txt += \
    """
==========================
Facade attributes overview
==========================
    """
    for csv_file in csv_files:
        txt += \
f"""
:py:class:`~oemof.tabular.facades.{os.path.splitext(csv_file)[0]}`

.. csv-table::
  :delim: ,
  :header-rows: 1
  :file: facade_attributes/{csv_file}
"""
    with open(destination, "w") as file:
        file.write(txt)
