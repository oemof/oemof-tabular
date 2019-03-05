import os
import pkg_resources as pkg
import pandas as pd

from oemof.solph import EnergySystem, Model, Bus
import oemof.tabular.tools.postprocessing as pp
import oemof.tabular.facades as fc


# datapath for input data from the oemof tabular pacakge
datapath = pkg.resource_filename("oemof.tabular", "examples/data/data.xls")

# results path for output
results_path = os.path.join(
    os.path.expanduser("~"), "oemof-results", "dispatch", "output"
)

if not os.path.exists(results_path):
    os.makedirs(results_path)

timeseries = pd.read_excel(
    datapath, sheet_name="timeseries", index_col=[0], parse_dates=True
)
timeseries.index.freq = "1H"

es = EnergySystem(timeindex=timeseries.index)

bus = Bus(label="DE")
es.add(bus)

es.add(
    fc.Volatile(
        label="wind",
        carrier="wind",
        tech="onshore",
        capacity=150,
        bus=bus,
        profile=timeseries["onshore"],
    )
)

es.add(
    fc.Dispatchable(
        label="ccgt",
        bus=bus,
        carrier="gas",
        tech="ccgt",
        capacity=100,
        marginal_cost=25,
    )
)

es.add(
    fc.Storage(
        label="storage",
        bus=bus,
        carrier="lithium",
        tech="battery",
        capacity=20,
        marginal_cost=5,
        balanced=True,
        initial_storage_capacity=1,
        storage_capacity=100,
    )
)

es.add(
    fc.Load(label="load", bus=bus, amount=500e3, profile=timeseries["load"])
)

es.add(fc.Excess(label="excess", bus=bus))

# create model based on energy system and its components
m = Model(es)

# write lp file
m.write(
    os.path.join(results_path, "dispatch.lp"),
    io_options={"symbolic_solver_labels": True},
)

#  solve the model using cbc solver
m.solve("cbc")

# write results back to the model object
m.results = m.results()

# writing results with the standard oemof-tabular output formatt
pp.write_results(m, results_path)

print("Optimization done. Results are in {}.".format(results_path))
