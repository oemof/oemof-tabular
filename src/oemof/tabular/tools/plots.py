import os

# import plotly.offline as offline
try:
    from matplotlib import colors
    from matplotlib.ticker import EngFormatter
except ImportError:
    raise ImportError("Need to install matplotlib to use plots!")

try:
    import plotly.graph_objs as go
except ImportError:
    raise ImportError("Need to install plotly to use plots!")

import pandas as pd

import numpy as np

# offline.init_notebook_mode()
from oemof.tabular.config.colors import CARRIER_COLER_MAP, TECH_COLOR_MAP

color = dict(TECH_COLOR_MAP, **CARRIER_COLER_MAP)

for t in TECH_COLOR_MAP:
    for c in CARRIER_COLER_MAP:
        color["-".join([c, t])] = TECH_COLOR_MAP[t]

color_dict = {name: colors.to_hex(color) for name, color in color.items()}


def hourly_plot(
    scenario,
    bus,
    datapath="results",
    flexibility=None,
    aggregate=None,
    daily=False,
    plot_filling_levels=True,
    title=None,
):
    """
    """
    if title is None:
        title = "Hourly supply and demand in {} for model/scenario {}".format(
            bus, scenario
        )
    if flexibility is None:
        flexibility = [
            "import",
            "acaes",
            "phs",
            "lithium-battery",
            "battery",
            "storage",
            "heat-storage",
        ]

    if aggregate is None:
        aggregate = [
            "coal",
            "lignite",
            "oil",
            "gas",
            "waste",
            "uranium",
            "wind",
            "solar",
        ]

    df, filling_levels = _load_results_sequences(scenario, datapath, bus, plot_filling_levels)

    df = _prepare_results_sequences(df, bus, aggregate, daily)

    x = df.index

    # create plot
    layout = go.Layout(
        barmode="stack",
        title=title,
        yaxis=dict(
            title="Energy in MWh",
            titlefont=dict(size=16, color="rgb(107, 107, 107)"),
            tickfont=dict(size=14, color="rgb(107, 107, 107)"),
        ),
        yaxis2=dict(
            title="Energy in MWh",
            overlaying="y",
            rangemode="tozero",
            autorange=True,
            side="right",
            showgrid=False,
        ),
    )

    data = []

    for c in df:
        if c in flexibility:
            data.append(
                go.Scatter(
                    x=x,
                    y=df[c].clip(lower=0),
                    name=c,
                    stackgroup="positive",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                )
            )
            data.append(
                go.Scatter(
                    x=x,
                    y=df[c].clip(upper=0),
                    name=c,
                    stackgroup="negative",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                    showlegend=False,
                )
            )

        elif "load" in c:
            # append load
            data.append(
                go.Scatter(
                    x=x, y=df[c], name=c, line=dict(width=3, color="darkred")
                )
            )
        elif "excess" in c:
            pass
        else:
            data.append(
                go.Scatter(
                    x=x,
                    fillcolor=color_dict.get(c, "black"),
                    y=df[c],
                    name=c,
                    stackgroup="positive",
                    line=dict(width=0, color=color_dict.get(c, "black")),
                )
            )

    if plot_filling_levels:
        for f in filling_levels:
            data.append(
                go.Scatter(
                    x=x,
                    y=filling_levels[f].values,
                    name=f + "-level",
                    yaxis="y2",
                    marker=dict(color="#d3560e"),
                )
            )

    return {"data": data, "layout": layout}


def plot_dispatch(ax, df, df_demand, unit, colors=None, linewidth=1):
    r"""
    Plots data as a dispatch plot. The demand is plotted as a line plot and
    suppliers and other consumers are plotted with a stackplot. Columns with negative vlaues
    are stacked below the x axis and columns with positive values above.

    Parameters
    ---------------
    ax : matplotlib.AxesSubplot
        Axis on which data is plotted.
    df : pandas.DataFrame
        Dataframe with data except demand.
    df_demand : pandas.DataFrame
        Dataframe with demand data.
    unit: string
        String with unit sign of plotted data on y-axis.
    colors_odict : collections.OrderedDictionary
        Ordered dictionary with labels as keys and colourcodes as values.
    linewidth: float
        Width of the line - set by default to 1.
    """
    assert not df.empty, "DataFrame is empty. Cannot plot empty data."
    assert (
        not df.columns.duplicated().any()
    ), "Cannot plot DataFrame with duplicate columns."

    if colors is None:
        colors = color_dict

    _check_undefined_colors(df.columns, colors.keys())

    # apply EngFormatter on axis
    ax = _eng_format(ax, unit=unit)

    # plot stackplot, differentiate between positive and negative stacked data
    y_stack_pos = []
    y_stack_neg = []

    # assign data to positive or negative stackplot
    for key, values in df.iteritems():
        stackgroup = _assign_stackgroup(key, values)
        if stackgroup == "negative":
            y_stack_neg.append(key)
        elif stackgroup == "positive":
            y_stack_pos.append(key)

    for i in y_stack_pos:
        if df[i].isin([0]).all():
            y_stack_pos.remove(i)

    # plot if there is positive data
    if not df[y_stack_pos].empty:
        stackplot(ax, df[y_stack_pos], colors)

    # plot if there is negative data
    if not df[y_stack_neg].empty:
        stackplot(ax, df[y_stack_neg], colors)

    # plot lineplot (demand)
    lineplot(ax, df_demand, colors, linewidth)


def plot_grouped_bar(ax, df, color_dict, unit, stacked=False):
    r"""
    This function plots scalar data as grouped bar plot. The index of the DataFrame
    will be interpreted as groups (e.g. regions), the columns as different categories (e.g. energy
    carriers) within the groups which will be plotted in different colors.

    Parameters
    ----------
    ax: matplotlib Axes object
        Axes to draw the plot.
    df: pd.DataFrame
        DataFrame with an index defining the groups and columns defining the bars of different color
        within the group.
    color_dict: dict
        Dictionary defining colors of the categories
    unit: str
        Unit of the variables.
    stacked : boolean
        Stack bars of a group. False by default.
    """
    alpha = 0.3
    # apply EngFormatter if power is plotted
    ax = _eng_format(ax, unit)

    df.plot.bar(
        ax=ax,
        color=[color_dict[key] for key in df.columns],
        width=0.8,
        zorder=2,
        stacked=stacked,
        rot=0,
    )

    ax.minorticks_on()
    ax.tick_params(axis="both", which="both", length=0, pad=7)

    ax.grid(axis="y", zorder=1, color="black", alpha=alpha)
    ax.grid(axis="y", which="minor", zorder=1, color="darkgrey", alpha=alpha)
    ax.set_xlabel(xlabel=None)
    ax.legend()
    ax.legend(title=None, frameon=True, framealpha=1)

    return ax


def stackplot(ax, df, colors_odict):
    r"""
    Plots data as a stackplot. The stacking order is determined by the order
    of labels in the colors_odict. It is stacked beginning with the x-axis as
    the bottom.

    Parameters
    ---------------
    ax : matplotlib.AxesSubplot
        Axis on which data is plotted.
    df : pandas.DataFrame
        Dataframe with data.
    colors_odict : collections.OrderedDictionary
        Ordered dictionary with labels as keys and colourcodes as values.
    """
    assert not df.empty, "Dataframe is empty."

    _check_undefined_colors(df.columns, colors_odict.keys())

    # y is a list which gets the correct stack order from colors file
    colors = []
    labels = []
    y = []

    order = list(colors_odict)

    for i in order:
        if i not in df.columns:
            continue
        labels.append(i)
        colors.append(colors_odict[i])
        y.append(df[i])

    y = np.vstack(y)
    ax.stackplot(df.index, y, colors=colors, labels=labels)


def lineplot(ax, df, colors_odict, linewidth=1):
    r"""
    Plots data as a lineplot.

    Parameters
    ---------------
    ax : matplotlib.AxesSubplot
        Axis on which data is plotted.
    df : pandas.DataFrame
        Dataframe with data.
    colors_odict : collections.OrderedDictionary
        Ordered dictionary with labels as keys and colourcodes as values.
    linewidth: float
        Width of the line - set by default to 1.
    """
    _check_undefined_colors(df.columns, colors_odict.keys())

    for i in df.columns:
        ax.plot(df.index, df[i], color=colors_odict[i], linewidth=linewidth, label=i)


def stacked_plot(scenario, datapath=None):
    """
    """

    df = pd.read_csv(
        os.path.join(datapath, scenario, "output", "capacities.csv"),
        index_col=0,
    )

    df = df.groupby(["to", "carrier", "tech"]).sum().unstack("to")
    df.index = ["-".join(i) for i in df.index]

    for i in ["coal", "lignite", "oil", "gas", "waste", "uranium"]:
        group = [c for c in df.index if i in c]
        df.loc[i] = df.loc[group].sum(axis=0)
        df.drop(group, axis=0, inplace=True)

    df.columns = df.columns.droplevel(0)

    return {
        "data": [
            go.Bar(
                x=row.index,
                y=row.values,
                name=idx,
                marker=dict(color=color_dict.get(idx, "black")),
            )
            for idx, row in df.iterrows()
        ],
        "layout": go.Layout(
            barmode="stack",
            title="Installed capacities for scenario {}".format(scenario),
        ),
    }


def _check_undefined_colors(labels, color_labels):
    undefined_colors = list(set(labels).difference(color_labels))

    if undefined_colors:
        raise KeyError(f"Undefined colors {undefined_colors}.")


def _eng_format(ax, unit):
    r"""
    Applies the EngFormatter to y-axis.

    Parameters
    ---------------
    ax : matplotlib.AxesSubplot
        Axis on which data is plotted.
    unit : string
        Unit which is plotted on y-axis

    Returns
    ----------
    ax : matplotlib.AxesSubplot
        Axis with formatter set to EngFormatter
    """
    formatter0 = EngFormatter(unit=unit)
    ax.yaxis.set_major_formatter(formatter0)
    return ax


def _assign_stackgroup(key, values):
    r"""
    This function decides if data is supposed to be plotted on the positive or negative side of
    the stackplot. If values has both negative and positive values, a value error is raised.

    Parameters
    ---------------
    key : string
        Column name.
    values: pandas.Series
        Values of column.

    Returns
    ----------
    stackgroup : string
        String with keyword positive or negative.
    """
    if all(values <= 0):
        stackgroup = "negative"
    elif all(values >= 0):
        stackgroup = "positive"
    elif all(values == 0):
        stackgroup = "positive"
    else:
        raise ValueError(
            key,
            " has both, negative and positive values. But it should only have either one",
        )

    return stackgroup


def _load_results_sequences(scenario, datapath, bus, plot_filling_levels):
    if scenario.endswith(".csv"):
        df = pd.read_csv(scenario, index_col=[0], parse_dates=True)
    else:
        df = pd.read_csv(
            os.path.join(datapath, scenario, "output", bus + ".csv"),
            index_col=[0],
            parse_dates=True,
        )

    if plot_filling_levels:
        filling_levels = pd.read_csv(
            os.path.join(datapath, scenario, "output", "filling_levels.csv"),
            index_col=[0],
            parse_dates=True,
        )
    else:
        filling_levels = None

    return df, filling_levels


def _prepare_results_sequences(df, bus, aggregate, daily):
    for i in aggregate:
        group = [c for c in df.columns if i in c]
        df[i] = df[group].sum(axis=1)
        df.drop(group, axis=1, inplace=True)

    # remove all zero columns
    df = df.loc[:, (df != 0).any(axis=0)]

    if daily:
        df = df.resample("1D").mean()

    # kind of a hack to get only the technologies
    df.columns = [c.replace(bus + "-", "") for c in df.columns]

    # strip also if only country code is part of supply name like ("DE-coal")
    if bus[0:2].isupper():
        df.columns = [c.replace(bus[0:3], "") for c in df.columns]

    return df
