# -*- coding: utf-8 -*-
"""
"""

import errno
import json
import os
import shutil

from datapackage import Package
import pandas as pd

from .building import package_from_resources, write_elements, write_sequences


def copy_datapackage(source, destination, subset=None):
    """
    Parameters
    ----------
    source: str
        datapackage.json
    destination: str
        Destination of copied datapackage
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


def clean_datapackage(path=None, directories=["data", "cache", "resources"]):
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
        shutil.rmtree(d, ignore_errors=True)


def to_dict(value):
    """ Convert value from e.g. csv-reader to valid json / dict
    """
    if value == "":
        return {}
    else:
        return json.loads(value)


def merge_packages(
    p1,
    p2,
    destpath,
    target_bus=None,
    inserted_bus=None,
    name=None,
    how=None,
    refm={
        "dispatchable-generator": "capacity",
        "volatile-generator": "capacity",
        "demand": "amount",
        "transshipment": None,
        "pumped-storage": ["capacity", "power"],
    },
):
    """
    Parameters
    ----------
    p1: string
        Path to datapackage.json of package to insert in `p2`
    p2: string
        Path to datapackage.json of package where `p1` data should be inserted
    destpath: string
        Path to destination directory.
    target_bus: string
        The name of the bus where the `insereted_bus` should be connceted to.
    inserted_bus: string
        The name of the bus that should be inserted / connected to target bus.
    name: string
        Name of new (merged) datapackage
    how: string
        How the merge should take place. Default is None which will simply
        merge the resources. Options are `techwise` and `elementwise` (1:1)
    refm: dict
        Resource-element-field mapper. Used for substraction etc. The dict
        specifies which field should be merged for a specific resource.

    Examples:
    ---------

    merge_packages(p1='/home/user/Bordelum/datapackage.json',
                   p2='/home/user/e-highway/datapackage.json',
                   target_bus='DE-electricity',
                   inserted_bus='Bordelum-electricity',
                   name='merged-package',
                   how='techwise')

    """

    # args = locals()
    # TODO Log function call.

    # TODO: Get target and inserted bus from the transshipment resource if
    # not provided...
    if target_bus is None:
        pass
    if inserted_bus is None:
        pass

    package1 = Package(p1)
    package2 = Package(p2)

    if name is None:
        name = (
            package1.descriptor.get(name, "unkown1")
            + "-"
            + package2.descriptor.get(name, "unkown2")
            + "-merged"
        )

    destpath = os.path.abspath(destpath)
    directories = set(
        [os.path.dirname(r.descriptor["path"]) for r in package1.resources]
    )

    for d in directories:
        os.makedirs(os.path.join(destpath, d))

    for r in package1.resources:
        #  check if resource from p1 exists in p2
        if r.name in package2.resource_names:
            print("Resource `{}` exists. Merging resources...".format(r.name))

            r1_df = pd.DataFrame(
                package1.get_resource(r.name).read(keyed=True)
            )
            r2_df = pd.DataFrame(
                package2.get_resource(r.name).read(keyed=True)
            )

            if os.path.dirname(r.descriptor["path"]) == "data/elements":
                if how == "techwise":
                    if refm.get(r.name) is not None:
                        for tech in r1_df["tech"].unique():
                            r2_df.loc[
                                (r2_df["bus"] == target_bus)
                                & (r2_df["tech"] == tech),
                                refm[r.name],
                            ] = r2_df.loc[
                                (r2_df["bus"] == target_bus)
                                & (r2_df["tech"] == tech),
                                refm[r.name],
                            ].values - sum(
                                r1_df.loc[
                                    (r1_df["bus"] == inserted_bus)
                                    & (r1_df["tech"] == tech),
                                    refm[r.name],
                                ].values
                            )
                elif how == "elementwise":
                    if refm.get(r.name) is not None:
                        for name in r1_df["name"]:
                            r2_df.loc[
                                (r2_df["bus"] == target_bus)
                                & (r2_df["name"] == name),
                                refm[r.name],
                            ] = (
                                r2_df.loc[
                                    (r2_df["bus"] == target_bus)
                                    & (r2_df["name"] == name),
                                    refm[r.name],
                                ].values
                                - r1_df.loc[
                                    (r1_df["bus"] == inserted_bus)
                                    & (r1_df["name"] == name),
                                    refm[r.name],
                                ].values
                            )
                else:
                    pass

                write_elements(
                    r.name + ".csv",
                    pd.concat([r1_df, r2_df]).set_index("name"),
                    directory=os.path.join(destpath, "data/elements"),
                    replace=True,
                )
                # TODO: Update meta data for the newly created resource...

            # if sequences, just merge, as no subtraction etc. is necessary
            elif os.path.dirname(r.descriptor["path"]) == "data/sequences":
                r1_df.set_index("timeindex", inplace=True)
                r2_df.set_index("timeindex", inplace=True)
                write_sequences(
                    r.name + ".csv",
                    pd.concat([r1_df, r2_df], axis=1),
                    directory=os.path.join(destpath, "data/sequences"),
                    replace=True,
                )
                # TODO: Update meta data for the newly created resource...

            # same for geometries as for sequences ?
            elif os.path.dirname(r.descriptor["path"]) == "data/geometries":
                # TODO: merge geometries
                pass

        # if resource does not exist as file, just copy this file and add meta
        # data to the datapackage.json file
        else:
            print(
                (
                    "Resource `{}` does not exist in package `{}`. "
                    + "Adding resource..."
                ).format(r.name, package2.descriptor.get("name", "unknown"))
            )

            rpath = os.path.join(destpath, r.descriptor["path"])

            pd.DataFrame(r.read(keyed=True)).to_csv(rpath, index=False)

            # add resource meta data
            package2.add_resource(r.descriptor)
            package2.commit()

    package2.save(os.path.join(destpath, "datapackage.json"))
    print("Merge successfull. Merged-package destination: {}".format(destpath))


# merge_packages(p1='/home/simnh/projects/Bordelum/datapackage.json',
#                p2='/home/simnh/projects/e-highway/datapackage.json',
#                target_bus='DE-electricity',
#                inserted_bus='Bordelum-electricity',
#                name='merged-package',
#                how='techwise')
