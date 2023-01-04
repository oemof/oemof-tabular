# -*- coding: utf-8 -*-
"""
The code in this module is partly based on third party code which has been
licensed under  GNU-GPL3. The following functions are copied and adapted from:

https://github.com/FRESNA/vresutils,
Copyright 2015-2017 Frankfurt Institute for Advanced Studies

* _shape2poly()
* simplify_poly()
* nuts()
"""
import os
from collections import OrderedDict
from functools import partial
from itertools import product, takewhile
from operator import attrgetter, itemgetter

import pandas as pd

try:
    from shapely.geometry import LinearRing, MultiPolygon, Polygon, shape
    from shapely.ops import transform
    from shapely.prepared import prep
except ImportError:
    raise ImportError("Need to install shapely to use geometry module!")

try:
    import pyproj
except ImportError:
    raise ImportError("Need to install pyproj to use geometry module!")

try:
    from geojson import Feature, FeatureCollection, dump, load
except ImportError:
    raise ImportError("Need to install geojson to use geometry module!")

try:
    import scipy.sparse as sparse
except ImportError:
    raise ImportError("Need to install scipy to use geometry module!")

try:
    import shapefile
except ImportError:
    raise ImportError("Need to install pyshp to use geometry module!")

import numpy as np


def read_geometries(filename, directory="data/geometries"):
    """
    Reads geometry resources from the datapackage. Data may either be stored
    in geojson format or as WKT representation in CSV-files.

    Parameters
    ----------
    filename: string
        Name of the elements to be read, for example `buses.geojson`
    directory: string
        Directory where the file is located. Default: `data/geometries`

    Returns
    -------
    pd.Series
    """

    path = os.path.join(directory, filename)

    if os.path.splitext(filename)[1] == ".geojson":
        if os.path.exists(path):
            with open(path, "r") as infile:
                features = load(infile)["features"]
                names = [f["properties"]["name"] for f in features]
                geometries = [shape(f["geometry"]) for f in features]
                geometries = pd.Series(dict(zip(names, geometries)))

    if os.path.splitext(filename)[1] == ".csv":
        if os.path.exists(path):
            geometries = pd.read_csv(path, sep=";", index_col=["name"])
        else:
            geometries = pd.Series(name="geometry")
            geometries.index.name = "name"

    return geometries


def write_geometries(filename, geometries, directory="data/geometries"):
    """Writes geometries to filesystem.

    Parameters
    ----------
    filename: string
        Name of the geometries stored, for example `buses.geojson`
    geometries: pd.Series
        Index entries become name fields in GeoJSON properties.
    directory: string
        Directory where the file is stored. Default: `data/geometries`

    Returns
    -------
    path: string
        Returns the path where the file has been stored.
    """

    path = os.path.join(directory, filename)

    if os.path.splitext(filename)[1] == ".geojson":
        features = FeatureCollection(
            [
                Feature(geometry=v, properties={"name": k})
                for k, v in geometries.iteritems()
            ]
        )

        if os.path.exists(path):
            with open(path) as infile:
                existing_features = load(infile)["features"]

            names = [f["properties"]["name"] for f in existing_features]

            assert all(i not in names for i in geometries.index), (
                "Cannot " "create duplicate entries in %s." % filename
            )

            features["features"] += existing_features

        with open(path, "w") as outfile:
            dump(features, outfile)

    if os.path.splitext(filename)[1] == ".csv":
        if os.path.exists(path):
            existing_geometries = read_geometries(filename, directory)
            geometries = pd.concat(
                [existing_geometries, geometries], verify_integrity=True
            )

        geometries.index.name = "name"

        geometries.to_csv(path, sep=";", header=True)

    return path


def _shape2poly(sh, tolerance=0.03, minarea=0.03, projection=None):
    """

    Notes
    -----
    Copied from: https://github.com/FRESNA/vresutils,
    Copyright 2015-2017 Frankfurt Institute for Advanced Studies
    """
    if len(sh.points) == 0:
        return None

    if projection is None:
        pts = sh.points
    elif projection == "invwgs":
        pts = np.asarray(
            _shape2poly.wgs(*np.asarray(sh.points).T, inverse=True)
        ).T
    else:
        raise TypeError("Unknown projection {}".format(projection))

    minlength = 2 * np.pi * np.sqrt(minarea / np.pi)

    def parts2polys(parts):
        rings = list(map(LinearRing, parts))
        while rings:
            exterior = rings.pop(0)
            interiors = list(takewhile(attrgetter("is_ccw"), rings))
            rings = rings[len(interiors) :]
            yield Polygon(
                exterior, [x for x in interiors if x.length > minlength]
            )

    polys = sorted(
        parts2polys(np.split(pts, sh.parts[1:])),
        key=attrgetter("area"),
        reverse=True,
    )
    mainpoly = polys[0]
    mainlength = np.sqrt(mainpoly.area / (2.0 * np.pi))
    if mainpoly.area > minarea:
        mpoly = MultiPolygon(
            [
                p
                for p in takewhile(lambda p: p.area > minarea, polys)
                if mainpoly.distance(p) < mainlength
            ]
        )
    else:
        mpoly = mainpoly
    return simplify_poly(mpoly, tolerance)


_shape2poly.wgs = pyproj.Proj(
    "+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84" " +units=m +no_defs"
)


def simplify_poly(poly, tolerance):
    """
    Notes
    -----
    Copied from: https://github.com/FRESNA/vresutils,
    Copyright 2015-2017 Frankfurt Institute for Advanced Studies
    """
    if tolerance is None:
        return poly
    else:
        return poly.simplify(tolerance, preserve_topology=True)


def nuts(filepath=None, nuts=0, subset=None, tolerance=0.03, minarea=1.0):
    """
    Reads shapefile with nuts regions and converts to polygons

    Returns
    -------
    OrderedDict
        Country keys as keys of dict and shapely polygons as corresponding
        values

    Notes
    -----
    Copied from: https://github.com/FRESNA/vresutils,
    Copyright 2015-2017 Frankfurt Institute for Advanced Studies
    """
    sf = shapefile.Reader(filepath)
    nuts = OrderedDict(
        sorted(
            [
                (rec[0], _shape2poly(sh, tolerance, minarea))
                for rec, sh in zip(sf.iterRecords(), sf.iterShapes())
                if rec[1] == nuts
            ],
            key=itemgetter(0),
        )
    )

    return nuts


def reproject(
    geom, fr=pyproj.Proj(init="EPSG:4326"), to=pyproj.Proj(init="EPSG:25832")
):
    """
    Notes
    -----
    Copied and adapted from: https://github.com/FRESNA/vresutils,
    Copyright 2015-2017 Frankfurt Institute for Advanced Studies
    """
    reproject_pts = partial(pyproj.transform, fr, to)
    return transform(reproject_pts, geom)


def Shapes2Shapes(
    orig, dest, normed=True, equalarea=False, prep_first=True, **kwargs
):
    """
    Notes
    -----
    Copied from: https://github.com/FRESNA/vresutils,
    Copyright 2015-2017 Frankfurt Institute for Advanced Studies
    """
    if equalarea:
        dest = list(map(reproject, dest))
        orig = list(map(reproject, orig))

    if prep_first:
        orig_prepped = list(map(prep, orig))
    else:
        orig_prepped = orig

    transfer = sparse.lil_matrix((len(dest), len(orig)), dtype=np.float)
    for i, j in product(range(len(dest)), range(len(orig))):
        if orig_prepped[j].intersects(dest[i]):
            area = orig[j].intersection(dest[i]).area
            transfer[i, j] = area / dest[i].area

    # sum of input vectors must be preserved
    if normed:
        ssum = np.squeeze(np.asarray(transfer.sum(axis=0)), axis=0)
        for i, j in zip(*transfer.nonzero()):
            transfer[i, j] /= ssum[j]

    return transfer


def intersects(geom, labels, geometries):
    """ """
    for label, geom_to_check in zip(labels, geometries):
        if geom.intersects(geom_to_check):
            return label
    return float("NaN")
