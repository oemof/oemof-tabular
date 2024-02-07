""" Tools to deserialize energy systems from datapackages.

**WARNING**

This is work in progress and still pretty volatile, so use it at your own risk.
The datapackage format and conventions we use are still a bit in flux. This is
also why we don't have documentation or tests yet. Once things are stabilized a
bit more, the way in which we extend the datapackage spec will be documented
along with how to use the functions in this module.

"""

import collections.abc as cabc
import json
import re
import typing
import warnings
from decimal import Decimal
from itertools import chain, groupby, repeat

import datapackage as dp
import pandas as pd
from oemof.network.network import Bus, Component

from oemof.tabular.config.config import supported_oemof_tabular_versions

from ..tools import HSN, raisestatement, remap

DEFAULT = object()
FLOW_TYPE = object()


def sequences(r, timeindices=None):
    """Parses the resource `r` as a sequence."""
    result = {
        name: [
            float(s[name]) if isinstance(s[name], Decimal) else s[name]
            for s in r.read(keyed=True)
        ]
        for name in r.headers
    }
    if timeindices is not None:
        timeindices[r.name] = result["timeindex"]
    result = {name: result[name] for name in result if name != "timeindex"}
    return result


def read_facade(
    facade,
    facades,
    create,
    typemap,
    data,
    objects,
    sequence_names,
    fks,
    resources,
):
    """Parse the resource `r` as a facade."""
    # TODO: Generate better error messages, if keys which are assumed to be
    # present, e.g. because they are used as foreign keys or because our
    # way of reading data packages needs them, are missing.
    if "name" in facade and facade["name"] in facades:
        return facades[facade["name"]]
    for field, reference in fks.items():
        if reference["resource"] in sequence_names:
            # if referenc not found -> set field value to None
            facade[field] = data[reference["resource"]].get(facade[field])
        elif facade[field][reference["fields"]] in objects:
            facade[field] = objects[facade[field][reference["fields"]]]
        elif facade[field][reference["fields"]] in facades:
            facade[field] = facades[facade[field][reference["fields"]]]
        else:
            foreign_keys = {
                fk["fields"]: fk["reference"]
                for fk in (
                    resources(reference["resource"])
                    .descriptor["schema"]
                    .get("foreignKeys", ())
                )
            }
            facade[field] = read_facade(
                facade[field],
                facades,
                create,
                typemap,
                data,
                objects,
                sequence_names,
                foreign_keys,
                resources,
            )
    # TODO: Do we really want to strip whitespace?
    mapping = typemap.get(facade.get("type").strip())
    if mapping is None:
        raise (
            ValueError(
                "Typemap is missing a mapping for '{}'.".format(
                    facade.get("type", "<MISSING TYPE>")
                )
            )
        )
    instance = create(mapping, facade, facade)
    facades[facade["name"]] = instance
    return instance


def deserialize_energy_system(cls, path, typemap={}, attributemap={}):
    cast_error_msg = (
        "Metadata structure of resource `{}` does not match data "
        "structure. Check the column names, types and their order."
    )

    default_typemap = {
        "bus": Bus,
        "hub": Bus,
        DEFAULT: Component,
        FLOW_TYPE: HSN,
    }

    for k, value in default_typemap.items():
        typemap[k] = typemap.get(k, value)

    if attributemap.get(object) is None:
        attributemap[object] = {"name": "label"}

    for k, value in attributemap.items():
        if value.get("name") is None:
            attributemap[k]["name"] = "label"

    package = dp.Package(path)
    # This is necessary because before reading a resource for the first
    # time its `headers` attribute is `None`.
    for r in package.resources:
        try:
            r.read()
        except dp.exceptions.CastError as e:
            raise dp.exceptions.CastError(
                "\n"
                + (cast_error_msg).format(r.name)
                + "\n"
                + "\n ".join([str(i) for i in e.errors])
            )
    empty = HSN()
    empty.read = lambda *xs, **ks: ()
    empty.headers = ()

    # check version that was used to create metadata
    oemof_tabular_version = package.descriptor.get("oemof_tabular_version")

    if oemof_tabular_version not in supported_oemof_tabular_versions:
        warnings.warn(
            f"Version of datapackage '{oemof_tabular_version}' is not "
            f"supported. These versions are supported: "
            f"{supported_oemof_tabular_versions}"
        )

    def parse(s):
        return json.loads(s) if s else {}

    data = {}

    def listify(x, n=None):
        return (
            x if isinstance(x, list) else repeat(x) if not n else repeat(x, n)
        )

    def resource(r):
        return package.get_resource(r) or empty

    timeindices = {}

    for r in package.resources:
        if all(
            re.match(r"^data/sequences/.*$", p)
            for p in listify(r.descriptor["path"], 1)
        ):
            data.update({r.name: sequences(r, timeindices)})
    sequence_names = set(data.keys())

    data.update(
        {
            name: {
                r["name"]: {key: r[key] for key in r}
                for r in resource(name).read(keyed=True)
            }
            for name in ("hubs", "components")
        }
    )

    data["elements"] = {
        e["name"]: {
            "name": e["name"],
            "inputs": {
                source: edges[i, source] for i, source in enumerate(inputs)
            },
            "outputs": {
                target: edges[i, target]
                for i, target in enumerate(outputs, len(inputs))
            },
            "parameters": dict(
                chain(
                    parse(e.get("node_parameters", "{}")).items(),
                    data["components"].get(e["name"], {}).items(),
                )
            ),
            "type": e["type"],
        }
        for e in resource("elements").read(keyed=True)
        for inputs, outputs in (
            (
                [p.strip() for p in e["predecessors"].split(",") if p],
                [s.strip() for s in e["successors"].split(",") if s],
            ),
        )
        for triples in (
            chain(
                *(
                    zip(
                        enumerate(chain(inputs, outputs)),
                        repeat(parameter),
                        listify(value),
                    )
                    for parameter, value in parse(
                        e.get("edge_parameters", "{}")
                    ).items()
                )
            ),
        )
        for edges in (
            {
                group: {
                    parameter: value
                    for _, parameter, value in grouped_triples
                    if value is not None
                }
                for group, grouped_triples in groupby(
                    sorted(triples), key=lambda triple: triple[0]
                )
            },
        )
    }

    def resolve_foreign_keys(source):
        """Check whether any key in `source` is a FK and follow it.

        The `source` dictionary is checked for whether any of
        its keys is a foreign key. A key is considered a
        foreign key if:

          - the value it points to is a string,
          - it is the name of a resource,
          - the value it points to is itself a top level key in
            the named resource.

        If the above is the case, the foreign key itself is
        deleted, the value it pointed to becomes the new key in
        it's place and the value the key points to in the named
        resource becomes the new value.
        Foreign keys are resolved deeply, i.e. if `source`
        contains nested dictionaries, foreign keys found on
        arbitrary levels are resolved.
        """
        for key in source:
            if (
                isinstance(source[key], str)
                and key in data
                and source[key] in data[key]
            ):
                source[key] = data[key][source[key]]

            if isinstance(source[key], cabc.MutableMapping):
                resolve_foreign_keys(source[key])

        return source

    resolve_foreign_keys(data["elements"])

    bus_names = set(
        chain(
            *(
                e[io].keys()
                for e in data["elements"].values()
                for io in ["inputs", "outputs"]
            )
        )
    )
    data["buses"] = {
        name: {
            "name": name,
            "type": (data["hubs"].get(name, {}).get("type", "bus")),
            "parameters": data["hubs"].get(name, {}),
        }
        for name in bus_names
    }

    objects = {}

    def create(cls, init, attributes):
        """Creates an instance of `cls` and sets `attributes`."""
        init.update(attributes)
        instance = cls(**remap(init, attributemap, cls))
        for k, v in remap(attributes, attributemap, cls).items():
            if not hasattr(instance, k):
                setattr(instance, k, v)
            name = getattr(instance, "name", getattr(instance, "label", None))
            if name is not None:
                objects[name] = instance
        return instance

    data["buses"] = {
        name: create(
            (
                mapping
                if mapping
                else raisestatement(
                    ValueError,
                    "Typemap is missing a mapping for '{}'.".format(
                        bus.get("type", "bus")
                    ),
                )
            ),
            {"label": name},
            bus["parameters"],
        )
        for name, bus in sorted(data["buses"].items())
        for mapping in (typemap.get(bus.get("type", "bus")),)
    }

    def resolve_object_references(source, f=None):
        """
        Check whether any key in `source` is a reference to a `name`d object.
        """

        def find(n, d):
            found = []
            for resource in d:
                if n in d[resource]:
                    assert getattr(d[resource][n], "label", n) == n
                    found.append(d[resource][n])
                assert len(found) <= 1
            return found

        filtered = {r: data[r] for r in data if (not f) or f(r)}
        for key, name in source.items():
            found = find(key, filtered)
            if len(found) > 0:
                v = source[key]
                del source[key]
                key = found[0]
                source[key] = v
            if isinstance(name, str):
                found = find(name, filtered)
                if len(found) > 0:
                    source[key] = found[0]

            if isinstance(source[key], cabc.MutableMapping):
                resolve_object_references(source[key], f=f)

        return source

    data["components"] = {
        name: create(
            typemap[element.get("type", DEFAULT)],
            {
                "label": name,
                "inputs": {
                    data["buses"][bus]: flow(
                        **remap(kwargs, attributemap, flow)
                    )
                    for bus, kwargs in sorted(element["inputs"].items())
                },
                "outputs": {
                    data["buses"][bus]: flow(
                        **remap(kwargs, attributemap, flow)
                    )
                    for bus, kwargs in sorted(element["outputs"].items())
                },
            },
            resolve_object_references(
                element["parameters"], f=lambda r: r == "buses"
            ),
        )
        for name, element in sorted(data["elements"].items())
        for flow in (typemap.get(FLOW_TYPE, HSN),)
    }

    period_data = {}
    if package.get_resource("periods"):
        df_periods = pd.DataFrame.from_dict(
            package.get_resource("periods").read(keyed=True)
        )
        period_data["timeincrement"] = df_periods["timeincrement"].values
        period_data["timeindex"] = pd.DatetimeIndex(df_periods["timeindex"])
        period_data["periods"] = [
            pd.DatetimeIndex(df["timeindex"])
            for period, df in df_periods.groupby("periods")
        ]
        period_data["periods"] = [
            pd.DatetimeIndex(i.values, freq=i.inferred_freq, name="timeindex")
            for i in period_data["periods"]
        ]
        period_data["years"] = period_data["timeindex"].year.unique().values

    def create_periodic_values(values, periods_index):
        """
        Create periodic values from given values and period_data.
        The values are repeated for each period for the whole length e.g.
        8760 values for hourly data in one period.

        Parameters
        ----------
        values : list
            List of values to be repeated.
        periods_index : list
            List containing periods datetimeindex.

        Returns
        -------
        list
            List of periodic values.
        """
        # check if length of list equals number of periods
        if len(values) != len(periods_index):
            raise ValueError(
                "Length of values does not equal number of periods."
            )

        # create timeseries with periodic values
        periodic_values = pd.concat(
            [
                pd.Series(repeat(values[i], len(period)), index=period)
                for i, period in enumerate(periods_index)
            ]
        )

        return periodic_values.tolist()

    def create_yearly_values(
        values: typing.Iterable[float], period_years: typing.Iterable[int]
    ):
        """
        Creates a value for every year (between two periods)
        Value of period is continued until next period
        Parameters
        ----------
        values values to be interpolated
        years years of periods

        Returns list
        -------

        """
        results = pd.Series()
        for i in range(len(period_years) - 1):
            diff = period_years[i + 1] - period_years[i]
            period_results = pd.Series(repeat(values[i], diff))
            results = pd.concat([results, period_results])
        results = pd.concat([results, pd.Series(values[-1])])
        return results.tolist()

    def unpack_sequences(facade, period_data):
        """
        Depending on dtype and content:
        Periodically changing values [given as array] are either unpacked into
            - full periods
            - yearly values (between periods)
            - kept as periodical values

        Decision happens based on
            - value
            - name
            - entry in yearly/periodical values list.

        Parameters
        ----------
        facade
        period_data

        Returns
        -------
        facade
        """

        yearly_values = ["fixed_costs", "marginal_costs"]
        periodical_values = [
            "capacity",
            "capacity_cost",
            "capacity_potential",
            "storage_capacity",
        ]

        for value_name, value in facade.items():
            if isinstance(value, Decimal):
                facade[value_name] = float(value)
            # check if multi-period and value is list
            if period_data and isinstance(value, list):
                # check if length of list equals number of periods
                if len(value) == len(period_data["periods"]):
                    if value_name in periodical_values:
                        # special period parameters don't need to be
                        # converted into timeseries
                        facade[value_name] = [
                            float(vv) if isinstance(vv, Decimal) else vv
                            for vv in value
                        ]
                        continue
                    elif value_name in yearly_values:
                        # special period parameter need to be
                        # converted into timeseries with value for each
                        # year
                        facade[value_name] = create_yearly_values(
                            value, period_data["years"]
                        )
                        msg = (
                            f"\nThe parameter '{value_name}' of a "
                            f"'{facade['type']}' facade is converted "
                            "into a yearly list. This might not be "
                            "possible for every parameter and lead to "
                            "ambiguous error messages.\nPlease be "
                            "aware, when using this feature!"
                        )
                        warnings.warn(msg, UserWarning)

                    else:
                        # create timeseries with periodic values
                        facade[value_name] = create_periodic_values(
                            value, period_data["periods"]
                        )
                        msg = (
                            f"\nThe parameter '{value_name}' of a "
                            f"'{facade['type']}' facade is converted "
                            "into a periodic timeseries. This might "
                            "not be possible for every parameter and "
                            "lead to ambiguous error messages.\nPlease"
                            " be aware, when using this feature!"
                        )
                        warnings.warn(msg, UserWarning)
        return facade

    facades = {}
    for r in package.resources:
        if all(
            re.match(r"^data/elements/.*$", p)
            for p in listify(r.descriptor["path"], 1)
        ):
            try:
                facade_data = r.read(keyed=True, relations=True)
            except dp.exceptions.CastError:
                raise dp.exceptions.LoadError((cast_error_msg).format(r.name))
            except Exception as e:
                raise dp.exceptions.LoadError(
                    (
                        "Could not read data for resource with name `{}`. "
                        " Maybe wrong foreign keys?\n"
                        "Exception was: {}"
                    ).format(r.name, e)
                )

            foreign_keys = {
                fk["fields"]: fk["reference"]
                for fk in r.descriptor["schema"].get("foreignKeys", ())
            }

            for facade in facade_data:
                # convert decimal to float

                read_facade(
                    unpack_sequences(facade=facade, period_data=period_data),
                    facades,
                    create,
                    typemap,
                    data,
                    objects,
                    sequence_names,
                    foreign_keys,
                    resource,
                )

    # TODO: Find concept how to deal with timeindices and clean up based on
    # concept
    lst = [idx for idx in timeindices.values()]
    if lst[1:] == lst[:-1]:
        # look for temporal resource and if present, take as timeindex from it
        if package.get_resource("temporal"):
            temporal = (
                pd.DataFrame.from_dict(
                    package.get_resource("temporal").read(keyed=True)
                )
                .set_index("timeindex")
                .astype(float)
            )
            # for correct freq setting of timeindex
            temporal.index = pd.DatetimeIndex(
                temporal.index.values,
                freq=temporal.index.inferred_freq,
                name="timeindex",
            )
            timeindex = temporal.index
            es = cls(timeindex=timeindex, temporal=temporal)

        # if no temporal provided as resource, take the first timeindex
        # from dict
        else:
            # look for periods resource and if present, take periods from it
            if package.get_resource("periods"):
                # look for tsa_parameters resource and if present, get
                # tsa_parameters from it
                # currently only works for multi-period
                if package.get_resource("tsa_parameters"):
                    df_tsa_parameters = pd.DataFrame.from_dict(
                        package.get_resource("tsa_parameters").read(keyed=True)
                    ).set_index("period", drop=True)

                    es = cls(
                        timeindex=period_data["timeindex"],
                        timeincrement=period_data["timeincrement"],
                        periods=period_data["periods"],
                        tsa_parameters=df_tsa_parameters.sort_index().to_dict(
                            "records"
                        ),
                        infer_last_interval=False,
                    )
                else:
                    es = cls(
                        timeindex=period_data["timeindex"],
                        timeincrement=period_data["timeincrement"],
                        periods=period_data["periods"],
                        infer_last_interval=False,
                    )

            # if lst is not empty
            elif lst:
                idx = pd.DatetimeIndex(lst[0])
                timeindex = pd.DatetimeIndex(
                    idx.values, freq=idx.inferred_freq, name="timeindex"
                )
                temporal = None
                es = cls(timeindex=timeindex, temporal=temporal)
            # if for any reason lst of datetimeindices is empty
            # (i.e. no sequences) have been provided, set datetime to one time
            # step of today (same as in the EnergySystem __init__ if no
            # timeindex is passed)
            else:
                timeindex = pd.date_range(
                    start=pd.to_datetime("today"), periods=1, freq="H"
                )
                es = cls(timeindex=timeindex)

        es.add(
            *chain(
                data["components"].values(),
                data["buses"].values(),
                facades.values(),
                chain(
                    *[
                        f.subnodes
                        for f in facades.values()
                        if hasattr(f, "subnodes")
                    ]
                ),
            )
        )

        es.typemap = typemap

        return es

    else:
        raise ValueError("Timeindices in resources differ!")


def deserialize_constraints(model, path, constraint_type_map=None):
    if constraint_type_map is None:
        constraint_type_map = {}

    def listify(x, n=None):
        return (
            x if isinstance(x, list) else repeat(x) if not n else repeat(x, n)
        )

    package = dp.Package(path)

    # read all resources in data/constraints
    resources = []
    for r in package.resources:
        if all(
            re.match(r"^data/constraints/.*$", p)
            for p in listify(r.descriptor["path"], 1)
        ):
            resources.append(r)

    for resource in resources:
        resource_data = resource.read(keyed=True, relations=True)

        for rw in resource_data:
            constraint_type = rw["type"]

            constraint_facade = constraint_type_map[constraint_type]

            constraint = constraint_facade(**rw)

            # build constraint for each facade
            constraint.build_constraint(model)

    # return model
