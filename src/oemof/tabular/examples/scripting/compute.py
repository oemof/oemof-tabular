"""
"""
import os

from importlib.resources import files
from oemof.solph import EnergySystem, Model

import oemof.tabular.tools.postprocessing as pp

# DONT REMOVE THIS LINE!
from oemof.tabular import datapackage  # noqa
from oemof.tabular.constraint_facades import CONSTRAINT_TYPE_MAP
from oemof.tabular.facades import TYPEMAP

examples = ["dispatch", "investment", "foreignkeys", "emission_constraint"]
for example in examples:
    print("Running compute example with datapackage {}".format(example))

    # path to directory with datapackage to load
    datapackage_dir = os.path.join(files("oemof.tabular"), "examples/datapackages/{}".format(example))

    # create  path for results (we use the datapackage_dir to store results)
    results_path = os.path.join(
        os.path.expanduser("~"), "oemof-results", example, "output"
    )
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

    # add constraints from datapackage to the model
    m.add_constraints_from_datapackage(
        os.path.join(datapackage_dir, "datapackage.json"),
        constraint_type_map=CONSTRAINT_TYPE_MAP,
    )

    # if you want dual variables / shadow prices uncomment line below
    # m.receive_duals()

    # select solver 'gurobi', 'cplex', 'glpk' etc
    m.solve("cbc")

    results = m.results()
    # now we use the write results method to write the results in oemof-tabular
    # format
    pp.write_results(m, results, results_path)
