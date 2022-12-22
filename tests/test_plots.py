from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from oemof.tabular.tools import plots as otaplots

HERE = Path(__file__).parent
PATH_PLOT_DATA = HERE / "_files" / "plot_data"


def test_plot_dispatch():
    path_data = PATH_PLOT_DATA / "flows-bus-electricity.csv"
    data = pd.read_csv(path_data, header=[0], parse_dates=[0], index_col=[0])

    df = data.iloc[:, :1]
    df_demand = pd.DataFrame(data.iloc[:, 2])

    fig, ax = plt.subplots()
    otaplots.plot_dispatch(
        ax=ax, df=df, df_demand=df_demand, unit="W"
    )


def test_hourly_plot():
    pass

def test_plot_grouped_bar():
    otaplots.plot_grouped_bar()
