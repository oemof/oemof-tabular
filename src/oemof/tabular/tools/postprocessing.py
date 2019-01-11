# -*- coding: utf-8 -*-
"""
"""
import os

import numpy as np
import pandas as pd

from oemof.network import Bus, Sink
from oemof.solph.components import GenericStorage
from oemof.outputlib import views
from oemof.tabular import facades


def component_results(es, results, select="sequences"):
    """ Aggregated by component type
    """

    c = {}

    for k, v in es.typemap.items():
        if type(k) == str:
            if select == "sequences":
                _seq_by_type = [
                    views.node(results, n, multiindex=True).get("sequences")
                    for n in es.nodes
                    if isinstance(n, v) and not isinstance(n, Bus)
                ]
                # check if dataframes / series have been returned
                if any(
                    [
                        isinstance(i, (pd.DataFrame, pd.Series))
                        for i in _seq_by_type
                    ]
                ):
                    seq_by_type = pd.concat(_seq_by_type, axis=1)
                    c[str(k)] = seq_by_type

            if select == "scalars":
                _sca_by_type = [
                    views.node(results, n, multiindex=True).get("scalars")
                    for n in es.nodes
                    if isinstance(n, v) and not isinstance(n, Bus)
                ]

                if [x for x in _sca_by_type if x is not None]:
                    _sca_by_type = pd.concat(_sca_by_type)
                    c[str(k)] = _sca_by_type

    return c


def bus_results(es, results, select="sequences", concat=False):
    """ Aggregated for every bus of the energy system
    """
    br = {}

    buses = [b for b in es.nodes if isinstance(b, Bus)]

    for b in buses:
        if select == "sequences":
            bus_sequences = pd.concat(
                [
                    views.node(results, b, multiindex=True).get(
                        "sequences", pd.DataFrame()
                    )
                ],
                axis=1,
            )
            br[str(b)] = bus_sequences
        if select == "scalars":
            br[str(b)] = views.node(results, b, multiindex=True).get("scalars")

    if concat:
        if select == "sequences":
            axis = 1
        else:
            axis = 0
        br = pd.concat([b for b in br.values()], axis=axis)

    return br


def supply_results(
    types=[
        "dispatchable",
        "volatile",
        "conversion",
        "backpressure",
        "extraction",
        "storage",
        "generator",
        "reservoir",
    ],
    bus=None,
    results=None,
    es=None,
):
    """
    """
    selection = pd.DataFrame()

    for t in types:
        if issubclass(es.typemap[t], GenericStorage) \
                and es.typemap[t] is not facades.Reservoir:
            df = views.net_storage_flow(results, node_type=es.typemap[t])
            if df is not None:
                selection = pd.concat([selection, df], axis=1)
        else:
            df = views.node_output_by_type(results, node_type=es.typemap[t])
            if df is not None:
                selection = pd.concat([selection, df], axis=1)

    selection = selection.loc[
        :, (slice(None), [es.groups[b] for b in bus], ["flow", "net_flow"])
    ]
    return selection


def demand_results(types=["load"], bus=None, results=None, es=None):
    """
    """
    selection = pd.DataFrame()

    for t in types:
        selection = pd.concat(
            [
                selection,
                views.node_input_by_type(results, node_type=es.typemap[t]),
            ],
            axis=1,
        )

    selection = selection.loc[
        :, ([es.groups[b] for b in bus], slice(None), ["flow"])
    ]

    return selection

def write_results(m, output_path, raw=False, summary=True, scalars=True):
    """
    """
    def save(df, name, path=output_path):
        """ Helper for writing csv files
        """
        df.to_csv(os.path.join(path, name + ".csv"))

    buses = [b.label for b in m.es.nodes if isinstance(b, Bus)]

    link_results = component_results(m.es, m.results).get("link")
    if link_results is not None and raw:
        save(link_results, "links-oemof")

    imports = pd.DataFrame()
    for b in buses:
        supply = supply_results(results=m.results, es=m.es, bus=[b])
        supply.columns = supply.columns.droplevel([1, 2])

        demand = demand_results(results=m.results, es=m.es, bus=[b])
        excess = component_results(m.es, m.results, select="sequences")["excess"]

        if link_results is not None and m.es.groups[b] in list(
            link_results.columns.levels[0]
        ):
            ex = link_results.loc[:, (m.es.groups[b], slice(None), "flow")].sum(
                axis=1
            )
            im = link_results.loc[:, (slice(None), m.es.groups[b], "flow")].sum(
                axis=1
            )

            net_import = im - ex
            net_import.name = m.es.groups[b]
            imports = pd.concat([imports, net_import], axis=1)

            supply["import"] = net_import

        if m.es.groups[b] in demand.columns:
            _demand = demand.loc[:, (m.es.groups[b], slice(None), "flow")]
            _demand.columns = _demand.columns.droplevel([0, 2])
            supply = pd.concat([
                supply, _demand], axis=1)
        if m.es.groups[b] in excess.columns:
            _excess = excess.loc[:, (m.es.groups[b], slice(None), "flow")]
            _excess.columns = _excess.columns.droplevel([0, 2])
            supply = pd.concat([supply, _excess], axis=1)
        save(supply, b)
        save(imports, "import")

    try:
        all = bus_results(m.es, m.results, select="scalars", concat=True)
        all.name = "value"
        endogenous = all.reset_index()
        endogenous["tech"] = [
            getattr(t, "tech", np.nan) for t in all.index.get_level_values(0)
        ]

    except ValueError:
        endogenous = pd.DataFrame()

    d = dict()
    for node in m.es.nodes:
        if not isinstance(node, (Bus, Sink, facades.Shortage)):
            if getattr(node, "capacity", None) is not None:
                if isinstance(node, facades.TYPEMAP["link"]):
                    pass
                else:
                    key = (
                        node,
                        [n for n in node.outputs.keys()][0],
                        "capacity",
                        node.tech,
                    )  # for oemof logic
                    d[key] = {"value": node.capacity}
    exogenous = pd.DataFrame.from_dict(d, orient="index").dropna()
    exogenous.index = exogenous.index.set_names(["from", "to", "type", "tech"])

    capacities = (
        pd.concat([endogenous, exogenous.reset_index()])
        .groupby(["to", "tech"])
        .sum()
        .unstack("to")
    )
    capacities.columns = capacities.columns.droplevel(0)
    save(capacities, "capacities")

    duals = bus_results(m.es, m.results, concat=True).xs(
        "duals", level=2, axis=1
    )
    duals.columns = duals.columns.droplevel(1)
    duals = (duals.T / m.objective_weighting).T
    save(duals, "shadow_prices")

    filling_levels = views.node_weight_by_type(
        m.results, GenericStorage
    )
    filling_levels.columns = filling_levels.columns.droplevel(1)
    save(filling_levels, "filling_levels")
