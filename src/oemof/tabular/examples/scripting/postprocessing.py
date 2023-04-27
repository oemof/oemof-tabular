from importlib.resources import files
import os
from oemof.solph import EnergySystem, Model, views

import oemof.tabular.datapackage  # noqa
import oemof.tabular.tools.postprocessing as pp
from oemof.tabular.facades import TYPEMAP

examples = ["dispatch", "investment", "foreignkeys"]
for example in examples:
    print("Runnig postprocessing example with datapackage {}".format(example))
    es = EnergySystem.from_datapackage(
        os.path.join(files("oemof.tabular"), "examples/datapackages/{}/datapackage.json".format(example)),
        attributemap={},
        typemap=TYPEMAP,
    )

    es.timeindex = es.timeindex[0:5]

    m = Model(es)

    m.solve(solver="cbc")

    # skip foreignkeys example as not all buses are present
    if example != "foreignkeys":
        br = pp.bus_results(es, m.results(), select="scalars")

        if example == "investment":
            br["bus0"].xs([es.groups["bus0"], "invest"], level=[1, 2])

        pp.supply_results(results=m.results(), es=es, bus=["heat-bus"])

        pp.supply_results(results=m.results(), es=es, bus=["bus0", "bus1"])

        pp.demand_results(results=m.results(), es=es, bus=["bus0", "bus1"])

        pp.component_results(results=m.results(), es=es, select="sequences")

        pp.component_results(results=m.results(), es=es, select="scalars")

        views.node_input_by_type(
            m.results(), node_type=TYPEMAP["storage"], droplevel=[2]
        )
