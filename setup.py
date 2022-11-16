#!/usr/bin/env python
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

from glob import glob
from os.path import basename, dirname, join, splitext
import io
import re

from setuptools import find_packages, setup


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fh:
        return fh.read()


setup(
    name="oemof.tabular",
    version="0.0.2dev",
    license="BSD 3-Clause License",
    description="Load oemof energy systems from tabular data sources.",
    long_description="%s\n%s"
    % (
        re.compile("^.. start-badges.*^.. end-badges", re.M | re.S).sub(
            "", read("README.rst")
        ),
        re.sub(":[a-z]+:`~?(.*?)`", r"``\1``", read("CHANGELOG.rst")),
    ),
    author="Stephan Günther, Simon Hilpert, Martin Söthe",
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
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
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
        "datapackage==1.5.1",
        "tableschema==1.3.0",
        "oemof.solph @ git+https://git@github.com/oemof/oemof-solph@v0.4#egg=oemof.solph",
        "pandas>=0.22",
        "paramiko",
        "toml",
    ],
    extras_require={
        'cli': ['click'],
        'plots': ['plotly', 'matplotlib'],
        'aggregation': ['tsam'],
        'geometry': ['shapely', 'scipy', 'pyproj', 'geojson'],
    },
    entry_points={"console_scripts": ["ota = oemof.tabular.cli:main"]},
)
