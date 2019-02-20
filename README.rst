========
Overview
========

.. start-badges

|version| |commits-since| |supported-versions| |license|

|travis| |appveyor| |docs| |requires| |wheel|

|coveralls| |codecov| |scrutinizer| |codacy| |codeclimate|

.. |docs| image:: https://readthedocs.org/projects/oemof-tabular/badge/?style=flat
    :target: https://readthedocs.org/projects/oemof-tabular
    :alt: Documentation Status


.. |travis| image:: https://travis-ci.org/oemof/oemof-tabular.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/oemof/oemof-tabular

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/oemof/oemof-tabular?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/gnn/oemof-tabular

.. |requires| image:: https://requires.io/github/oemof/oemof-tabular/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/oemof/oemof-tabular/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof-tabular/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/oemof/oemof-tabular

.. |codecov| image:: https://codecov.io/github/oemof/oemof-tabular/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof-tabular

.. |codacy| image:: https://img.shields.io/codacy/grade/14dbd9b9c5e34f8b80e73887b5aa6e6c.svg
    :target: https://app.codacy.com/project/gnn/oemof-tabular/dashboard
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/oemof/oemof-tabular/badges/gpa.svg
   :target: https://codeclimate.com/github/oemof/oemof-tabular
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/oemof.tabular.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof.tabular

.. |commits-since| image:: https://img.shields.io/badge/dynamic/json.svg?label=%2B&url=https%3A%2F%2Fapi.github.com%2Frepos%2Foemof%2Foemof-tabular%2Fcompare%2Fv0.0.1...master&query=%24.total_commits&colorB=blue
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-tabular/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.tabular.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/oemof.tabular

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.tabular.svg
    :alt: Supported versions
    :target: https://pypi.org/project/oemof.tabular

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/oemof/oemof-tabular/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof-tabular/

.. |license| image:: https://img.shields.io/pypi/l/oemof-tabular.svg?colorB=blue
    :alt: PyPI - License
    :target: https://github.com/oemof/oemof-tabular/blob/master/LICENSE

.. end-badges

Load oemof energy systems from tabular data sources.

* Free software: BSD 3-Clause License

Installation
============

We are currently using features which haven't made it to a proper
`oemof` release yet. This means that you have to install `oemof.tabular`
from source, since `pip` `doesn't allow`_ packages on `PyPI` to have
dependencies which are not hosted on `PyPI`:

::

    pip install 'git+https://git@github.com/oemof/oemof-tabular.git'

You also need at least `pip` version `18.1` for this to work.

.. _doesn't allow: https://pip.pypa.io/en/stable/news/#id58

Documentation
=============


https://oemof-tabular.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
