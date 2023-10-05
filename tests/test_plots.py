from pathlib import Path

from matplotlib.testing.compare import compare_images
import matplotlib.pyplot as plt
import pandas as pd

from oemof.solph.helpers import extend_basic_path

from oemof.tabular.tools import plots as otaplots

HERE = Path(__file__).parent
PATH_PLOT_DATA = HERE / "_files" / "plot_data"
PATH_PLOTS = HERE / "_files" / "plots"
TEMP_PATH_PLOTS = Path(extend_basic_path("tmp_plots"))


def compare_plots(filename, tol=0):
    expected_plot = PATH_PLOTS / filename
    temp_plot = TEMP_PATH_PLOTS / filename
    plt.savefig(temp_plot)
    assert not compare_images(expected_plot, temp_plot, tol=tol, in_decorator=False), "Plots do not match!"


def test_plot_dispatch():
    path_data = PATH_PLOT_DATA / "flows-bus-electricity.csv"
    data = pd.read_csv(path_data, header=[0], parse_dates=[0], index_col=[0])

    df = data.iloc[:, :1]
    df_demand = pd.DataFrame(data.iloc[:, 2])

    fig, ax = plt.subplots()
    otaplots.plot_dispatch(
        ax=ax, df=df, df_demand=df_demand, unit="W"
    )
    compare_plots("plot_dispatch.png")


def test_hourly_plot():
    pass

def test_plot_grouped_bar():
    pass
    # otaplots.plot_grouped_bar()
