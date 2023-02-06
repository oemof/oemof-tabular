import dataclasses
import pandas as pd
from oemof.tabular.facades import TYPEMAP


def get_facade_attrs(TYPEMAP):
    facade_attrs = {}
    for key, facade in TYPEMAP.items():
        if dataclasses.is_dataclass(facade):
            fields = dataclasses.fields(facade)
            df = pd.DataFrame.from_dict(
                {
                    "name": [field.name for field in fields],
                    "type": [field.type.__name__ if hasattr(field.type, "__name__") else field.type for field in fields ],
                    "default": [None if isinstance(field.default, dataclasses._MISSING_TYPE) else None for field in fields],
                },
            )
            df = df.set_index("name")

            facade_attrs[key] = df

    return facade_attrs


def write_table_rst(destination, tables):
    txt = ""
    with open(destination, "w") as file:
        file.write(txt)
