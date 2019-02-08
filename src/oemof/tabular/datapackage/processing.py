# -*- coding: utf-8 -*-
"""
"""

import errno
import json
import os
import shutil

from datapackage import Package

from .building import package_from_resources


def copy_datapackage(source, destination, subset=None):
    """
    Parameters
    ----------
    source: str
        datapackage.json
    destination: str
        Destination of copied datapackage
    name (optional): str
        Name of datapackage
    only_data: str
        Name of directory to only copy subset of datapackage (for example
        only the 'data' directory)
   """
    if source.endswith(".json"):
        package_root = os.path.dirname(os.path.realpath(source))
        sp = Package(
            os.path.join(package_root, "datapackage.json")
        )  # source package
    else:
        raise ValueError("Set a path to a *.json meta-data file for copying.")

    try:
        if subset:
            shutil.copytree(
                os.path.join(package_root, subset),
                os.path.join(destination, subset),
            )
            # write new meta data for copied data
            p = Package(base_path=destination)
            p.infer(os.path.join(destination, "**/*.csv"))
            for r in p.resources:
                r.descriptor["schema"]["foreignKeys"] = (
                    sp.get_resource(r.name)
                    .descriptor["schema"]
                    .get("foreignKeys", [])
                )
                r.commit()
                r.save(
                    os.path.join(destination, "resources", r.name + ".json")
                )
            package_from_resources(
                output_path=destination,
                resource_path=os.path.join(destination, "resources"),
            )

        else:
            shutil.copytree(package_root, destination)
    except OSError as e:
        # If the error was caused because the source wasn't a directory
        if e.errno == errno.ENOTDIR:
            shutil.copy(package_root, destination)
        else:
            raise IOError("Directory not copied. Error: %s" % e)

    return destination


def clean(path=None, directories=["data", "cache", "resources"]):
    """
    Parameters
    ----------
    path: str
        Path to root directory of the datapackage, if no path is passed the
        current directory is to be assumed the root.
    directories: list (optional)
        List of directory names inside the root directory to clean (remove).
    """

    if not path:
        path = os.getcwd()

    for d in directories:
        shutil.rmtree(os.path.join(path, d), ignore_errors=True)


def to_dict(value):
    """ Convert value from e.g. csv-reader to valid json / dict
    """
    if value == "":
        return {}
    else:
        return json.loads(value)
