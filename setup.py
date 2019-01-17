#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

from glob import glob
from os.path import basename, dirname, join, splitext
import io
import re
import sys

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


setup(
    name="oemof.tabular",
    version="0.0.1dev",
    license="BSD 3-Clause License",
    description="Load oemof energy systems from tabular data sources.",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Stephan Günther, Simon Hilpert, Martin Söthe, Cord Kaldemeyer",
    author_email="gnn.code@gmail.com",
    url="https://github.com/oemof/oemof-tabular",
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
        "License :: OSI Approved :: BSD License",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
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
    install_requires=[
        "datapackage",
        "geojson",
        "oemof==0.2.4.dev0",
        "pandas>=0.22",
        "paramiko",
        "pyproj==1.9.5.1.dev0"
        if sys.version_info.major >= 3 and sys.version_info.minor >= 7
        else "pyproj",
        "pyshp",
        "scipy",
        "shapely",
        "tsam",
    ],
    extras_require={
        # eg:
        #   'rst': ['docutils>=0.11'],
        #   ':python_version=="2.6"': ['argparse'],
    },
    dependency_links=(
        [
            (
                "git+https://git@github.com/gnn/pyproj.git"
                "@69a26ce46634749f602518a375849999cb5e41e0"
                "#egg=pyproj-1.9.5.1.dev0"
            )
        ]
        if sys.version_info.major >= 3 and sys.version_info.minor >= 7
        else []
    )
    + [
        (
            "git+https://git@github.com/oemof/oemof.git"
            "@releases/v0_3_0"
            "#egg=oemof-0.2.4.dev0"
        )
    ],
)
