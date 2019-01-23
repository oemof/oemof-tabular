# -*- coding: utf-8 -*-
from ftplib import FTP
from urllib.parse import urlparse
import errno
import json
import os
import shutil
import tarfile
import urllib.request
import zipfile

from datapackage import Package, Resource, infer
from geojson import Feature, FeatureCollection, dump, load
from shapely.geometry import shape
import toml
import pandas as pd
import paramiko


def infer_resources(directory="data/elements"):
    """ Method looks at all files in `directory` and creates
    datapackage.Resource object that will be stored

    """
    if not os.path.exists("resources"):
        os.makedirs("resources")

    # create meta data resources
    for f in os.listdir(directory):
        r = Resource({"path": os.path.join(directory, f)})
        r.infer()
        r.save(os.path.join("resources", f.replace(".csv", ".json")))


def update_package_descriptor():
    """
    """
    p = Package("datapackage.json")

    for f in os.listdir("resources"):
        path = os.path.join("resources", f)

        r = Resource(path)

        p.add_resource(r.descriptor)

        p.commit()

        os.remove(path)

    os.rmdir("resources")

    p.save("datapackage.json")


def infer_metadata(
    package_name="default-name",
    keep_resources=False,
    foreign_keys={
        "bus": [
            "volatile",
            "dispatchable",
            "storage",
            "load",
            "reservoir",
            "shortage",
            "excess",
        ],
        "profile": ["load", "volatile", "ror"],
        "from_to_bus": ["connection", "line", "conversion"],
        "chp": ["backpressure", "extraction", "chp"],
    },
    path=None):
    """ Add basic meta data for a datapackage

    Parameters
    ----------
    package_name: string
        Name of the data package
    keep_resource: boolean
        Flag indicating of the resources meta data json-files should be kept
        after main datapackage.json is created. The reource meta data will
        be stored in the `resources` directory.
    foreign_keys: dict
        Dictionary with foreign key specification. Keys for dictionary are:
        'bus', 'profile', 'from_to_bus'. Values are list with
        strings with the name of the resources
    path: string
        Absoltue path to root-folder of the datapackage
    """
    current_path = os.getcwd()
    if path:
        print("Setting current work directory to {}".format(path))
        os.chdir(path)

    p = Package()
    p.descriptor["name"] = package_name
    p.descriptor["profile"] = "tabular-data-package"
    p.commit()
    if not os.path.exists("resources"):
        os.makedirs("resources")

    # create meta data resources elements
    if not os.path.exists("data/elements"):
        print(
            "No data path found in directory {}. Skipping...".format(
                os.getcwd())
        )
    else:
        for f in os.listdir("data/elements"):
            r = Resource({"path": os.path.join("data/elements", f)})
            r.infer()
            r.descriptor["schema"]["primaryKey"] = "name"

            if r.name in foreign_keys.get("bus", []):
                r.descriptor["schema"]["foreignKeys"] = [
                    {
                        "fields": "bus",
                        "reference": {"resource": "bus", "fields": "name"},
                    }
                ]

                if r.name in foreign_keys.get("profile", []):
                    r.descriptor["schema"]["foreignKeys"].append(
                        {
                            "fields": "profile",
                            "reference": {"resource": r.name + "_profile"},
                        }
                    )

            elif r.name in foreign_keys.get("from_to_bus", []):
                r.descriptor["schema"]["foreignKeys"] = [
                    {
                        "fields": "from_bus",
                        "reference": {"resource": "bus", "fields": "name"},
                    },
                    {
                        "fields": "to_bus",
                        "reference": {"resource": "bus", "fields": "name"},
                    },
                ]

            elif r.name in foreign_keys.get("chp", []):
                r.descriptor["schema"]["foreignKeys"] = [
                    {
                        "fields": "fuel_bus",
                        "reference": {"resource": "bus", "fields": "name"},
                    },
                    {
                        "fields": "electricity_bus",
                        "reference": {"resource": "bus", "fields": "name"},
                    },
                    {
                        "fields": "heat_bus",
                        "reference": {"resource": "bus", "fields": "name"},
                    },
                ]

            r.commit()
            r.save(os.path.join("resources", f.replace(".csv", ".json")))
            p.add_resource(r.descriptor)

    # create meta data resources elements
    if not os.path.exists("data/sequences"):
        print(
            "No data path found in directory {}. Skipping...".format(
                os.getcwd())
        )
    else:
        for f in os.listdir("data/sequences"):
            r = Resource({"path": os.path.join("data/sequences", f)})
            r.infer()
            r.commit()
            r.save(os.path.join("resources", f.replace(".csv", ".json")))
            p.add_resource(r.descriptor)

    p.commit()
    p.save("datapackage.json")

    if not keep_resources:
        shutil.rmtree("resources")

    os.chdir(current_path)


def package_from_resources(resource_path, output_path, clean=True):
    """ Collects resource descriptors and merges them in a datapackage.json

    Parameters
    ----------
    resource_path: string
        Path to directory with resources (in .json format)
    output_path: string
        Root path of datapackage where the newly created datapckage.json is
        stored
    clean: boolean
        If true, resources will be deleted
    """
    p = Package()

    p.descriptor["profile"] = "tabular-data-package"
    p.commit()

    for f in os.listdir(resource_path):
        path = os.path.join(resource_path, f)

        r = Resource(path)

        p.add_resource(r.descriptor)

        p.commit()

        os.remove(path)

    if clean:
        os.rmdir(resource_path)

    p.save(os.path.join(output_path, "datapackage.json"))


def _ftp(remotepath, localpath, hostname, username=None, passwd=""):
    """ Download data with FTP

    Parameters
    ----------
    remotepath: str
        The remote file to copy.
    localpath: str
        The destination path on localhost.
    hostname: str
        The server to connect to.
    username: str
        The username to authenticate as.
    passwd: str
        The password to authenticate with.
    """

    ftp = FTP(hostname)

    if username:
        ftp.login(user=username, passwd=passwd)
    else:
        ftp.login()

    ftp.retrbinary("RETR " + remotepath, open(localpath, "wb").write)
    ftp.quit()

    return


def _sftp(
    remotepath,
    localpath,
    hostname="",
    username="rutherford",
    password=""
):
    """ Download data with SFTP

    Parameters
    ----------
    remotepath: str
        The remote file to copy.
    localpath: str
        The destination path on localhost.
    hostname: str
        The server to connect to.
    username:
        The username to authenticate as.
    """

    client = paramiko.SSHClient()
    client.load_host_keys(os.path.expanduser("~/.ssh/known_hosts"))

    client.connect(hostname=hostname, username=username, password=password)

    sftp = client.open_sftp()
    sftp.get(remotepath, localpath)

    sftp.close()
    client.close()

    return


def _http(url, path):
    """ Download data with HTTP

    Parameters
    ----------
    url: str
        Url of file to be downloaded.
    path: str
        The destination path on localhost.
    """

    user_agent = (
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) "
        "Gecko/2009021910 "
        "Firefox/3.0.7")
    headers = {"User-Agent": user_agent}
    request = urllib.request.Request(url, None, headers)

    f = urllib.request.urlopen(request)
    data = f.read()
    with open(path, "wb") as code:
        code.write(data)

    return


def download_data(url, directory="cache", unzip_file=None, **kwargs):
    """
    Downloads data and stores it in specified directory

    Parameters
    ----------
    url: str
        Url of file to be downloaded.
    directory: str
        Name of directory where to store the downloaded data.
        Default is 'cache'-
    unzip_file: str
        Regular or directory file name to be extracted from zip source.
    kwargs:
        Additional keyword arguments.
    """

    scheme, netloc, path, params, query, fragment = urlparse(url)

    if not unzip_file:
        filepath = os.path.join(directory, os.path.basename(path))
        copypath = filepath
    else:
        filepath = os.path.join(directory, unzip_file)
        copypath = os.path.join(directory, os.path.basename(path))

    if os.path.exists(filepath):
        return filepath

    else:

        if scheme in ["http", "https"]:
            _http(url, copypath)

        elif scheme == "sftp":
            _sftp(path, copypath, hostname=netloc, **kwargs)

        elif scheme == "ftp":
            _ftp(path, copypath, hostname=netloc, **kwargs)

        else:
            raise ValueError(
                "Cannot download data. Not supported scheme \
                             in {}.".format(
                    url
                )
            )

    if unzip_file is not None:

        def member(x):
            return x.startswith(unzip_file.split("/")[0])

        if copypath.endswith(".zip"):
            zipped = zipfile.ZipFile(copypath, "r")
            if unzip_file.endswith("/"):
                zipped.extractall(
                    filepath, members=list(filter(member, zipped.namelist()))
                )
            else:
                zipped.extract(unzip_file, directory)

            zipped.close()

        elif copypath.endswith(".tar.gz"):
            tar = tarfile.open(copypath, "r:gz")
            if unzip_file.endswith("/"):
                tar.extractall(
                    filepath,
                    members=list(
                        filter(member, [t.name for t in tar.getmembers()])
                    ),
                )
            else:
                tar.extract(unzip_file, directory)

            tar.close()

        os.remove(copypath)

    return filepath


def timeindex(year, periods=8760, freq='H'):
    """ Create pandas datetimeindex.

    Parameters
    ----------
    year: string
        Year of the index
    periods: string
        Number of periods, default: 8760
    freq: string
        Freq of the datetimeindex, default: 'H'
    """

    idx = pd.date_range(start=year, periods=periods, freq=freq)

    return idx


def initialize(config, directory='.'):
    """ Initialize datapackage by reading config file and creating required
    directories (data/elements, data/sequences etc.) if directories are
    not specified in the config file, the default directory setup up
    will be used.

    """
    sub_directories = {
        "elements":  "data/elements",
        "sequences": "data/sequences",
        "geometries": "data/geometries",
    }

    if not config:
        try:
            default = "config.json"
            config = get_config(default)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Default path `{}` of config file not found!".format(default)
            )
    
    sub_directories.update(config.get("sub-directories", {}))

    for subdir in sub_directories.values():
        try:
            os.makedirs(os.path.join(directory, subdir))
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

    return sub_directories

def input_filepath(file, directory="archive/"):
    """
    """
    file_path = os.path.join(directory, file)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            """File with name

            {}

            does not exist. Please make sure you download the file from
            the sources listed and store it in the directory:

            {}.
            """.format(
                file_path, directory
            )
        )

    return file_path


def read_build_config(file="build.toml"):
    """ Read config build file in toml format

    Parameters
    ----------
    file: string
        String with name of config file
    """
    try:
            config = toml.load(file)

            # create paths
            if config.get("directories"):
                config["directories"] = {
                    k: os.path.join(os.getcwd(), v)
                    for k, v in config["directories"].items()
                }
    except Exception as e:
        raise ValueError("Could not load config file: {}".format(e))

    return config


def read_sequences(filename, directory="data/sequences"):
    """ Reads sequence resources from the datapackage

    Parameters
    ----------
    filename: string
        Name of the sequences to be read, for example `load_profile.csv`
    directory: string
        Directory from where the file should be read. Default: `data/sequences`
    """

    path = os.path.join(directory, filename)

    if os.path.exists(path):
        sequences = pd.read_csv(
            path, sep=";", index_col=["timeindex"], parse_dates=True
        )

    else:
        sequences = pd.DataFrame(columns=["timeindex"]).set_index("timeindex")

    return sequences


def read_elements(filename, directory="data/elements"):
    """
    Reads element resources from the datapackage

    Parameters
    ----------
    filename: string
        Name of the elements to be read, for example `load.csv`
    directory: string
        Directory where the file is located. Default: `data/elements`

    Returns
    -------
    pd.DataFrame
    """
    path = os.path.join(directory, filename)

    if os.path.exists(path):
        elements = pd.read_csv(path, sep=";")
        elements.set_index("name", inplace=True)
    else:
        elements = pd.DataFrame(columns=["name"]).set_index("name")

    return elements


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
    """ Writes geometries to filesystem.

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


def write_elements(filename, elements, directory="data/elements",
                   replace=False):
    """ Writes elements to filesystem.

    Parameters
    ----------
    filename: string
        Name of the elements to be read, for example `reservoir.csv`
    elements: pd.DataFrame
        Elements to be stored in data frame. Index: `name`
    directory: string
        Directory where the file is stored. Default: `data/elements`
    replace: boolean
        If set, existing data will be overwritten. Otherwise integrity of
        data (unique indices) will be checked
    Returns
    -------
    path: string
        Returns the path where the file has been stored.
    """

    path = os.path.join(directory, filename)

    if elements.index.name != "name":
        elements.index.name = "name"

    if not replace:
        existing_elements = read_elements(filename, directory=directory)
        elements = pd.concat(
            [existing_elements, elements], verify_integrity=True
        )

    elements = elements.reindex(sorted(elements.columns), axis=1)

    elements.reset_index(inplace=True)

    elements.to_csv(path, sep=";", quotechar="'", index=0)

    return path


def write_sequences(filename, sequences, directory= "data/sequences",
                    replace=False):
    """ Writes sequences to filesystem.

    Parameters
    ----------
    filename: string
        Name of the sequences to be read, for example `load_profile.csv`
    sequences: pd.DataFrame
        Sequences to be stored in data frame. Index: `datetimeindex` with
        format %Y-%m-%dT%H:%M:%SZ
    directory: string
        Directory where the file is stored. Default: `data/elements`
    replace: boolean
        If set, existing data will be overwritten. Otherwise integrity of
        data (unique indices) will be checked
    Returns
    -------
    path: string
        Returns the path where the file has been stored.
    """

    path = os.path.join(directory, filename)

    if sequences.index.name != "timeindex":
        sequences.index.name = "timeindex"

    if replace:
        sequences = sequences
    else:
        existing_sequences = read_sequences(filename, directory=directory)
        sequences = pd.concat(
            [existing_sequences, sequences], axis=1, verify_integrity=True
        )
        # TODO: Adapt to new build config file
        # if len(sequences.index.difference(timeindex())) > 0:
        #     raise ValueError(
        #         "Wrong timeindex for sequence {}.".format(filename)
        #     )

    sequences = sequences.reindex(sorted(sequences.columns), axis=1)

    sequences.to_csv(path, sep=";", date_format="%Y-%m-%dT%H:%M:%SZ")

    return path
