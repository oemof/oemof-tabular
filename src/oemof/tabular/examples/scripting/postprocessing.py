import pkg_resources as pkg

from oemof.outputlib import views
from oemof.solph import EnergySystem, Model
import oemof.tabular.tools.postprocessing as pp
from oemof.tabular.facades import TYPEMAP

examples = [
    # 'dispatch',
    # 'investment',
    "foreignkeys",
    # 'lopf'
]

for example in examples:
    print("Running example {}".format(example))
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

    m.solve(solver='cbc')

    # get bus results
    br = pp.bus_results(es, m.results(), select='scalars')

    # select on bus and reduce multiindex
    # br['bus0'].xs([es.groups['bus0'], 'invest'], level=[1, 2])

    pp.supply_results(results=m.results(), es=es, bus=['heat-bus'])

    pp.supply_results(results=m.results(), es=es, bus=['bus0', 'bus1'])

    pp.demand_results(results=m.results(), es=es, bus=['bus0', 'bus1'])

    pp.component_results(results=m.results(), es=es, select="sequences")

    pp.component_results(results=m.results(), es=es, select="scalars")

    views.node_input_by_type(
        m.results(), node_type=TYPEMAP['storage'], droplevel=[2]
    )


# views.node_output_by_type(m.results(), node_type=TYPEMAP['storage'],
#                          droplevel=[2])
#
# views.node_weight_by_type(m.results(), node_type=TYPEMAP['storage'])
#
# views.net_storage_flow(results=m.results(), node_type=TYPEMAP['storage'])
#
# views.node(processing.parameter_as_dict(es), es.nodes[0], multiindex=True)[
#     'scalars'
# ]

# pp.bus_results(es, m.results(), select='scalars', concat=True)
