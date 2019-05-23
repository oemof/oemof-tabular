import os

# import plotly.offline as offline
from matplotlib import colors
import pandas as pd
import plotly.graph_objs as go

# offline.init_notebook_mode()
from oemof.tabular.facades import CARRIER_COLER_MAP, TECH_COLOR_MAP

color = dict(TECH_COLOR_MAP, **CARRIER_COLER_MAP)

for t in TECH_COLOR_MAP:
    for c in CARRIER_COLER_MAP:
        color["-".join([c, t])] = TECH_COLOR_MAP[t]

color_dict = {name: colors.to_hex(color) for name, color in color.items()}


def hourly_plot(
    scenario,
    bus,
    datapath="results",
    flexibility=[
        "import",
        "acaes",
        "phs",
        "lithium-battery",
        "battery",
        "storage"
    ],
    aggregate=[
        "coal", "lignite", "oil", "gas", "waste", "uranium", "wind", "solar"],
    daily=False,
    plot_filling_levels=True,
):
    """
    """
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

    for i in aggregate:
        group = [c for c in df.columns if i in c]
        df[i] = df[group].sum(axis=1)
        df.drop(group, axis=1, inplace=True)

    # remove all zero columns
    df = df.loc[:, (df != 0).any(axis=0)]

    if daily:
        df = df.resample("1D").mean()

    x = df.index
    # kind of a hack to get only the technologies
    df.columns = [c.replace(bus + "-", "") for c in df.columns]
    # strip also if only country code is part of supply name like ("DE-coal")
    df.columns = [c.replace(bus[0:3], "") for c in df.columns]
    # create plot
    layout = go.Layout(
        barmode="stack",
        title="Hourly supply and demand in {} for model/scenario {}".format(
            bus, scenario
        ),
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
