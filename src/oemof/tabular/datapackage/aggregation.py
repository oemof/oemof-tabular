# -*- coding: utf-8 -*-
"""
Module used for aggregation sequences and elements.

"""
import os
import re

from datapackage import Package, Resource
import pandas as pd
import tsam.timeseriesaggregation as tsam

from .building import write_sequences
from .processing import copy_datapackage


def temporal_skip(datapackage, n, path="/tmp", name=None, *args):
    """ Creates a new datapackage by aggregating sequences inside the
    `sequence` folder of the specified datapackage by skipping `n` timesteps

    Parameters
    ----------
    datapackage: string
        String of meta data file datapackage.json
    n: integer
        Number of timesteps to skip
    path: string
        Path to directory where the aggregated datapackage is stored
    name: string
        Name of the new, aggregated datapackage. If not specified a name will
        be given
    """
    p = Package(datapackage)

    cwd = os.getcwd()

    if name is None:
        copied_package_name = (
            p.descriptor["name"] + "__temporal_skip__" + str(n)
        )
    else:
        copied_package_name = name

    copy_path = os.path.join(path, p.descriptor["name"])

    copied_root = copy_datapackage(
        datapackage, os.path.abspath(copy_path), subset="data"
    )

    sequence_resources = [
        r
        for r in p.resources
        if re.match(r"^data/sequences/.*$", r.descriptor["path"])
    ]

    dfs = {
        r.name: pd.DataFrame(r.read(keyed="True"))
        .set_index("timeindex")
        .astype(float)
        for r in sequence_resources
    }
    sequences = pd.concat(dfs.values(), axis=1)

    skip_sequences = sequences.loc[::n]

    temporal = pd.Series(data=n, index=skip_sequences.index, name="weighting")
    temporal.index.name = "timeindex"

    os.chdir(copied_root)

    for r in sequence_resources:
        write_sequences(
            r.name + ".csv", dfs[r.name].loc[temporal.index], replace=True
        )

    # write temporal information from clustering
    temporal.to_csv(
        "data/temporal.csv",
        header=True,
        sep=";",
        date_format="%Y-%m-%dT%H:%M:%SZ",
    )
    # add meta data for new temporal information
    r = Resource({"path": "data/temporal.csv"})
    r.infer()

    r.descriptor[
        "description"
    ] = "Temporal selection based on skipped timesteps. Skipped n={}".format(n)

    # Update meta-data of copied package
    cp = Package("datapackage.json")
    cp.descriptor["name"] = copied_package_name
    cp.descriptor["resources"].append(r.descriptor)
    cp.commit()
    cp.save("datapackage.json")

    # set back to 'old' workdirectory
    os.chdir(cwd)

    return copied_root


def temporal_clustering(datapackage, n, path="/tmp", how="daily"):
    """
    """
    if how == "weekly":
        raise NotImplementedError("Weekly clustering is not implemented!")

    p = Package(datapackage)

    cwd = os.getcwd()

    copied_package_name = (
        p.descriptor["name"] + "__temporal_cluster__" + how + "_" + str(n)
    )

    copy_path = os.path.join(path, p.descriptor["name"], copied_package_name)

    copied_root = copy_datapackage(
        datapackage, os.path.abspath(copy_path), subset="data"
    )

    sequence_resources = [
        r
        for r in p.resources
        if re.match(r"^data/sequences/.*$", r.descriptor["path"])
    ]

    dfs = {
        r.name: pd.DataFrame(r.read(keyed="True"))
        .set_index("timeindex")
        .astype(float)
        for r in sequence_resources
    }
    sequences = pd.concat(dfs.values(), axis=1)

    if how == "daily":
        hoursPerPeriod = 24
    elif how == "hourly":
        hoursPerPeriod = 1
    elif how == "weekly":
        hoursPerPeriod = 24 * 7

    aggregation = tsam.TimeSeriesAggregation(
        sequences,
        noTypicalPeriods=n,
        rescaleClusterPeriods=False,
        hoursPerPeriod=hoursPerPeriod,
        clusterMethod="hierarchical",
    )

    cluster_weights = {
        aggregation.clusterCenterIndices[n]: w
        for n, w in aggregation.clusterPeriodNoOccur.items()
    }
    if how == "daily":
        temporal = pd.Series(
            {
                d: cluster_weights[d.dayofyear]
                for d in sequences.index
                if d.dayofyear in aggregation.clusterCenterIndices
            },
            name="weighting",
        )
        temporal.index.name = "timeindex"

    elif how == "hourly":
        temporal = pd.Series(
            {
                h: cluster_weights[sequences.index.get_loc(h)]
                for h in sequences.index
                if sequences.index.get_loc(h)
                in aggregation.clusterCenterIndices
            },
            name="weighting",
        )
        temporal.index.name = "timeindex"

    # write resources to copied package (should not interfer with meta data)
    # as columns are not removed and sorted when written.
    os.chdir(copied_root)
    for r in sequence_resources:
        write_sequences(
            r.name + ".csv", dfs[r.name].loc[temporal.index], replace=True
        )

    # write temporal information from clustering
    temporal.to_csv(
        "data/temporal.csv",
        header=True,
        sep=";",
        date_format="%Y-%m-%dT%H:%M:%SZ",
    )
    # add meta data for new temporal information
    r = Resource({"path": "data/temporal.csv"})
    r.infer()
    # TODO: Add meta-data description
    r.descriptor[
        "description"
    ] = "Temporal selection based on hierachical clustering..."

    # Update meta-data of copied package
    cp = Package("datapackage.json")
    cp.descriptor["name"] = copied_package_name
    cp.descriptor["resources"].append(r.descriptor)
    cp.commit()
    cp.save("datapackage.json")

    # set back to 'old' workdirectory
    os.chdir(cwd)

    return copied_root


def loop_temporal(f, d, narray, *args):
    return [f(d, n, *args) for n in narray]
