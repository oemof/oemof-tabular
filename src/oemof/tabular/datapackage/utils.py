import dataclasses
import itertools
import warnings

import addict
import pandas as pd

from oemof.tabular.facades import TYPEMAP


class Data:
    """
    Implements the hierarchical data as in the filetree.

    data[][][] = resource
    """

    def __init__(self):
        self.data = addict.Dict()

    def set_resource(self, location, resource):
        d = nest_dict_from_lst(location, resource)
        self.data.update(d)

    def get_resource(self, location):
        result = self.data
        for item in location:
            result = result[item]
        return result

    def to_tuple_dict(self):
        return tuple_keys(self.data)


def get_facade_fields():

    facade_fields = {
        name: dataclasses.fields(facade)
        for name, facade in TYPEMAP.items()
        if dataclasses.is_dataclass(facade)
    }

    return facade_fields


def populate_df(df, **kwargs):
    undefined_keys = [key for key in kwargs if key not in df.columns]

    if any(undefined_keys):
        warnings.warn(f"There are undefined keys: {undefined_keys}")

    # perform cartesian product if lists are given
    given_values = {
        k: v if isinstance(v, list) else [v] for k, v in kwargs.items()
    }

    cartesian_product = pd.DataFrame(
        itertools.product(*given_values.values()), columns=given_values.keys()
    )

    # populate dataframe
    for col in cartesian_product.columns:
        df[col] = cartesian_product[col]

    return df


def tuple_keys(nested_dict):
    location_resource = {}

    def walk_dict(dictionary, location=None):
        if location is None:
            location = []
        for key, value in dictionary.items():
            where_am_i = location.copy()
            where_am_i.append(key)
            if isinstance(value, dict):
                walk_dict(value, location=where_am_i)
            else:
                location_resource[tuple(where_am_i)] = value

        return location_resource

    return walk_dict(nested_dict)


def nest_dict_from_lst(lst, resource):

    nested_dict = resource
    for key in reversed(lst):
        nested_dict = addict.Dict({key: nested_dict})

    return nested_dict
