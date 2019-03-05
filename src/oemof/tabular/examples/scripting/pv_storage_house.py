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
    os.path.expanduser("~"), "oemof-results", "pv-storage-household", "output"
)

if not os.path.exists(results_path):
    os.makedirs(results_path)

timeseries = pd.read_excel(
    datapath, sheet_name="timeseries", index_col=[0], parse_dates=True
)
timeseries.index.freq = "1H"

es = EnergySystem(timeindex=timeseries.index)

bus = Bus(label="household")
es.add(bus)

es.add(
    fc.Volatile(
        label="pv",
        carrier="solar",
        tech="pv",
        capacity=10,
        bus=bus,
        profile=timeseries["pv"],
        fixed=False,
    )
)

es.add(
    fc.Storage(
        label="storage",
        bus=bus,
        carrier="lithium",
        tech="battery",
        capacity=3,
        storage_capacity=12,
    )
)

# the connection to the grid is modelled by a shortage component
es.add(
    fc.Shortage(
        label="grid",
        bus=bus,
        carrier="electricity",
        tech="grid",
        capacity=100,
        marginal_cost=0.3,
    )
)

es.add(fc.Load(label="load", bus=bus, amount=20e3, profile=timeseries["load"]))

# create the model using the energy system with its components (see: es.nodes)
m = Model(es)

# solve model using cbc solver
m.solve("cbc")

pp.supply_results(bus=["household"], es=es, results=m.results())
