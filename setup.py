#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import io
import re
from glob import glob
from os.path import basename
from os.path import dirname
from os.path import join
from os.path import splitext

from setuptools import find_packages
from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


setup(
    name="oemof.datapackage",
    version="0.0.6.dev0",
    license="BSD-3-Clause",
    description="Load oemof energy systems from datapackage data sources.",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author=(
        "Stephan Günther, Simon Hilpert, Martin Söthe, Jann Launer, "
        "Hendrik Huyskens, Julian Endres, Felix Maurer"
    ),
    author_email="gnn.code@gmail.com",
    url="https://github.com/oemof/oemof-datapackage",
    packages=["oemof"] + ["oemof." + p for p in find_packages("src/oemof")],
    package_dir={"": "src"},
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        #
        #   http://pypi.python.org/pypi?%3Aaction=list_classifiers
        #
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        # uncomment if you test on these interpreters:
        # 'Programming Language :: Python :: Implementation :: IronPython',
        # 'Programming Language :: Python :: Implementation :: Jython',
        # 'Programming Language :: Python :: Implementation :: Stackless',
        "Topic :: Utilities",
    ],
    keywords=[
        # eg: 'keyword1', 'keyword2', 'keyword3',
    ],
    python_requires=">=3.9",
    install_requires=[
        "datapackage==1.5.1",
        "cchardet",
        "tableschema",  # newer versions (v1.8.0 and up) fail!
        "oemof.solph",
        "pandas>=0.22",
        "oemof.network",  # Temporal fix due to braking changes in 0.5.1
        "paramiko",
        "toml",
        "numpy",  # To be deleted with higher oemof.solph version
    ],
    extras_require={
        "cli": ["click"],
        "dev": ["pytest", "black", "isort", "flake8"],
        "plots": ["plotly", "matplotlib"],
        "aggregation": ["tsam"],
        "geometry": ["shapely", "scipy", "pyproj", "geojson", "pyshp"],
    },
    entry_points={"console_scripts": ["ota = oemof.datapackage.cli:main"]},
)
