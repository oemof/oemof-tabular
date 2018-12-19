# -*- coding: utf-8 -*-
"""
"""
import os

import pandas as pd

from oemof.network import Bus
from oemof.solph.components import GenericStorage
from oemof.outputlib import views, processing
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
                    sca_by_type = pd.concat(_sca_by_type)
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
        if isinstance(es.typemap[t], GenericStorage):
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
