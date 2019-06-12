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

from collections import OrderedDict
from functools import partial
from itertools import product, takewhile
from operator import attrgetter, itemgetter

from shapely.geometry import LinearRing, MultiPolygon, Polygon
from shapely.ops import transform
from shapely.prepared import prep
import numpy as np
import pyproj
import scipy.sparse as sparse
import shapefile


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
            rings = rings[len(interiors):]
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
    """
    """
    for label, geom_to_check in zip(labels, geometries):
        if geom.intersects(geom_to_check):
            return label
    return float("NaN")
