import dataclasses

import addict

from oemof.tabular.facades import TYPEMAP


def get_facade_fields():

    facade_fields = {
        name: dataclasses.fields(facade)
        for name, facade in TYPEMAP.items()
        if dataclasses.is_dataclass(facade)
    }

    return facade_fields


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
