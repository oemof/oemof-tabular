import os
import pkg_resources as pkg
import pandas as pd
import plotly.offline as offline

from oemof.solph import EnergySystem, Model, Bus
import oemof.tabular.tools.postprocessing as pp
import oemof.tabular.facades as fc


# datapath for input data from the oemof tabular pacakge
datapath = pkg.resource_filename(
    'oemof.tabular',
    'examples/data/data.xls')

# results path for output
results_path = os.path.join(
    os.path.expanduser('~'),
    "oemof-results",
    "dispatch",
    "output")

if not os.path.exists(results_path):
    os.makedirs(results_path)

timeseries = pd.read_excel(
    datapath,
    sheet_name="timeseries",
    index_col=[0],
    parse_dates=True)
timeseries.index.freq = "1H"

es = EnergySystem(timeindex=timeseries.index)

bus = Bus(label='DE')

wind = fc.Volatile(
    label='wind',
    carrier="wind",
    tech="onshore",
    capacity=150,
    bus=bus,
    profile=timeseries['onshore'])

ccgt = fc.Dispatchable(
    label='ccgt',
    bus=bus,
    carrier="gas",
    tech="ccgt",
    capacity=100,
    marginal_cost=25)

sto = fc.Storage(
    label='storage',
    bus=bus,
    carrier="lithium",
    tech="battery",
    capacity=20,
    storage_capacity=100,
    capacity_ratio=1/6
    )

load = fc.Load(
    label='load',
    bus=bus,
    amount=500e3,
    profile=timeseries['load'])

curtailment = fc.Excess(
    label="excess",
    bus=bus)

# add the components to the energy system object
es.add(wind, load, sto, ccgt, bus, curtailment)

# create model based on energy system and its components
m = Model(es)

#  solve the model using cbc solver
m.solve('cbc')

# write results back to the model object
m.results = m.results()

# writing results with the standard oemof-tabular output formatt
pp.write_results(m, results_path)


if False:
    from plots import hourly_plot, stacked_plot
    # plot results with plotly
    offline.plot(
        hourly_plot(
            'dispatch',
            'DE',
            os.path.join(
                os.path.expanduser('~'),
                "oemof-results")
            ),
        filename=os.path.join(results_path, 'hourly-plot.html'))


    # plot results with plotly
    offline.plot(
        stacked_plot(
            'dispatch',
            os.path.join(
                os.path.expanduser('~'),
                "oemof-results")
            ),
        filename=os.path.join(results_path, 'stacked-plot.html'))
