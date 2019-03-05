import os
import pkg_resources as pkg
import pandas as pd
import plotly.offline as offline


from oemof.solph import EnergySystem, Model, Bus
import oemof.tabular.tools.postprocessing as pp
from oemof.tools.economics import annuity
import oemof.tabular.facades as fc
from oemof.solph.constraints import emission_limit


# datapath for input data from the oemof tabular pacakge
datapath = pkg.resource_filename("oemof.tabular", "examples/data/data.xls")

# results path for output
results_path = os.path.join(
    os.path.expanduser("~"), "oemof-results", "investment", "output"
)

if not os.path.exists(results_path):
    os.makedirs(results_path)

timeseries = pd.read_excel(
    datapath, sheet_name="timeseries", index_col=[0], parse_dates=True
)
timeseries.index.freq = "1H"

costs = pd.read_excel(datapath, sheet_name="costs", index_col=[0])

es = EnergySystem(timeindex=timeseries.index)
setattr(es, "typemap", fc.TYPEMAP)

bus = Bus(label="DE")

wind = fc.Volatile(
    label="wind",
    bus=bus,
    carrier="wind",
    tech="onshore",
    capacity_cost=annuity(
        costs.at["capex", "onshore"],
        costs.at["lifetime", "onshore"],
        costs.at["wacc", "onshore"],
    ),
    profile=timeseries["onshore"],
)

pv = fc.Volatile(
    label="pv",
    bus=bus,
    carrier="solar",
    tech="pv",
    capacity_cost=annuity(
        costs.at["capex", "pv"],
        costs.at["lifetime", "pv"],
        costs.at["wacc", "pv"],
    ),
    profile=timeseries["pv"],
)

ccgt = fc.Dispatchable(
    label="ccgt",
    bus=bus,
    carrier="gas",
    tech="ccgt",
    capacity_cost=annuity(
        costs.at["capex", "ccgt"],
        costs.at["lifetime", "ccgt"],
        costs.at["wacc", "ccgt"],
    ),
    output_parameters={"emission_factor": 0.2 / 0.55},
    marginal_cost=25 / 1000,
)

sto = fc.Storage(
    label="storage",
    bus=bus,
    carrier="electricity",
    tech="battery",
    capacity_cost=annuity(
        costs.at["capex", "storage"],
        costs.at["lifetime", "storage"],
        costs.at["wacc", "storage"],
    ),
    capacity_ratio=1 / 6,
)

load = fc.Load(label="load", bus=bus, amount=500e6, profile=timeseries["load"])

curtailment = fc.Excess(label="excess", bus=bus)
# add the components to the energy system object
es.add(wind, pv, load, sto, ccgt, bus, curtailment)

# create model based on energy system and its components
m = Model(es)
emission_limit(m, limit=5e6)

#  solve the model using cbc solver
m.solve("cbc")

# write results back to the model object
m.results = m.results()

# writing results with the standard oemof-tabular output formatt
pp.write_results(m, results_path)

# plot results with plotly
if True:
    from oemof.tabular.tools.plots import hourly_plot

    offline.plot(
        hourly_plot(
            "investment",
            "DE",
            os.path.join(os.path.expanduser("~"), "oemof-results"),
        ),
        filename=os.path.join(results_path, "hourly-plot.html"),
    )
