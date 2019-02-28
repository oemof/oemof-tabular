"""
"""
import os
import pkg_resources as pkg

from oemof.solph import EnergySystem, Model
import oemof.tabular.tools.postprocessing as pp
from oemof.tabular.facades import TYPEMAP

name = 'investment'

# path to directory with datapackage to load
datapackage_dir = pkg.resource_filename(
    'oemof.tabular',
    'examples/datapackages/{}'.format(name)
)

# create  path for results (we use the datapackage_dir to store results)
results_path = os.path.join(
    os.path.expanduser('~'), "oemof-results", name)
if not os.path.exists(results_path):
    os.makedirs(results_path)

# create energy system object
es = EnergySystem.from_datapackage(
    os.path.join(datapackage_dir, "datapackage.json"),
    attributemap={},
    typemap=TYPEMAP,
)

# create model from energy system (this is just oemof.solph)
m = Model(es)

# if you want dual variables / shadow prices uncomment line below
# m.receive_duals()

# select solver 'gurobi', 'cplex', 'glpk' etc
m.solve('cbc')

# get the results from the the solved model(still oemof.solph)
m.results = m.results()

# now we use the write results method to write the results in oemof-tabular
# format
pp.write_results(m, results_path)
