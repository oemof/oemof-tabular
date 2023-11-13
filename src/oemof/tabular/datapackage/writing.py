import pandas as pd
from oemof.solph.helpers import flatten

exclude_attrs = []
exclude_none = True


def move_undetected_scalars(com):
    # copied from oemof.solph.processing
    for ckey, value in list(com["sequences"].items()):
        if isinstance(value, str):
            com["scalars"][ckey] = value
            del com["sequences"][ckey]
            continue
        try:
            _ = (e for e in value)
        except TypeError:
            com["scalars"][ckey] = value
            del com["sequences"][ckey]
        else:
            try:
                if not value.default_changed:
                    com["scalars"][ckey] = value.default
                    del com["sequences"][ckey]
            except AttributeError:
                pass


def remove_nones(com):
    # copied from oemof.solph.processing
    for ckey, value in list(com["scalars"].items()):
        if value is None:
            del com["scalars"][ckey]
    for ckey, value in list(com["sequences"].items()):
        if len(value) == 0 or value[0] is None:
            del com["sequences"][ckey]


def detect_scalars_and_sequences(com):
    # copied from oemof.solph.processing
    com_data = {"scalars": {}, "sequences": {}}

    default_exclusions = [
        "__",
        "_",
        "registry",
        "inputs",
        "outputs",
        "Label",
        "input",
        "output",
        "constraint_group",
    ]
    # Must be tuple in order to work with `str.startswith()`:
    exclusions = tuple(default_exclusions + exclude_attrs)
    attrs = [
        i
        for i in dir(com)
        if not (callable(getattr(com, i)) or i.startswith(exclusions))
    ]

    for a in attrs:
        attr_value = getattr(com, a)

        # Iterate trough investment and add scalars and sequences with
        # "investment" prefix to component data:
        if attr_value.__class__.__name__ == "Investment":
            invest_data = detect_scalars_and_sequences(attr_value)
            com_data["scalars"].update(
                {
                    "investment_" + str(k): v
                    for k, v in invest_data["scalars"].items()
                }
            )
            com_data["sequences"].update(
                {
                    "investment_" + str(k): v
                    for k, v in invest_data["sequences"].items()
                }
            )
            continue

        if isinstance(attr_value, str):
            com_data["scalars"][a] = attr_value
            continue

        # If the label is a tuple it is iterable, therefore it should be
        # converted to a string. Otherwise, it will be a sequence.
        if a == "label":
            attr_value = str(attr_value)

        # check if attribute is iterable
        # see: https://stackoverflow.com/questions/1952464/
        # in-python-how-do-i-determine-if-an-object-is-iterable
        try:
            _ = (e for e in attr_value)
            com_data["sequences"][a] = attr_value
        except TypeError:
            com_data["scalars"][a] = attr_value

    com_data["sequences"] = flatten(com_data["sequences"])
    move_undetected_scalars(com_data)
    if exclude_none:
        remove_nones(com_data)

    com_data = {
        "scalars": pd.Series(com_data["scalars"]),
        "sequences": pd.DataFrame(com_data["sequences"]),
    }
    return com_data


def get_inputs_outputs(component, attr):
    if hasattr(component, attr):
        return getattr(component, attr)
    else:
        return {}


def get_connected_busses(component):
    inputs = list(get_inputs_outputs(component, "inputs"))
    outputs = list(get_inputs_outputs(component, "outputs"))

    def formatting(lst, name):
        return {
            (f"bus_{n}", name, None): str(bus) for n, bus in enumerate(lst)
        }

    connected_busses = formatting(inputs, "inputs")
    connected_busses.update(formatting(outputs, "outputs"))

    connected_busses = pd.Series(connected_busses, name="var_value")
    return connected_busses


def serialize_energysystem(energysystem, path):
    from pathlib import Path

    import oemof.network

    components = [
        node
        for node in energysystem.nodes
        if isinstance(node, oemof.network.Component)
    ]
    types = {}

    # group components by type and number of inputs/outputs
    for component in components:
        typ = type(component).__name__

        # find out number of inputs and outputs
        n_inputs = len(get_inputs_outputs(component, "inputs"))
        n_outputs = len(get_inputs_outputs(component, "outputs"))

        key = (typ, n_inputs, n_outputs)

        if typ not in types:
            types[key] = []

        component_data = detect_scalars_and_sequences(component)

        component_data = component_data["scalars"]
        # set index
        index = pd.DataFrame(component_data.index, columns=["0"])
        index["1"] = None
        index["2"] = None
        index = pd.MultiIndex.from_frame(index)
        component_data.index = index
        component_data.name = "var_value"

        busses = get_connected_busses(component)

        data = pd.concat([component_data, busses], axis=0)

        types[key].append(data)

        # TODO: flow_data = get_flow_data(component)

        # TODO: Handle sequences with foreign keys

    # save data to destination
    for typ, data in types.items():
        filepath = Path(path) / f"{typ}.csv"
        df = pd.DataFrame(data)
        df.to_csv(filepath)
