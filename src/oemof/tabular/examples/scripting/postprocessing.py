import pkg_resources as pkg

from oemof.outputlib import views
from oemof.solph import EnergySystem, Model

from oemof.tabular.facades import TYPEMAP
import oemof.tabular.datapackage
import oemof.tabular.tools.postprocessing as pp


examples = ["dispatch", "investment", "foreignkeys"]
for example in examples:
    print("Runnig postprocessing example with datapackage {}".format(example))
    es = EnergySystem.from_datapackage(
        pkg.resource_filename(
            'oemof.tabular',
            'examples/datapackages/{}/datapackage.json'.format(example),
        ),
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
