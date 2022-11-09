========
Overview
========

.. start-badges

|version| |commits-since| |supported-versions| |license|

|docs| |wheel| |coveralls| |codecov| |codeclimate|


.. |docs| image:: https://readthedocs.org/projects/oemof-tabular/badge/?style=flat
    :target: https://readthedocs.org/projects/oemof-tabular
    :alt: Documentation Status

.. |coveralls| image:: https://coveralls.io/repos/oemof/oemof-tabular/badge.svg?branch=dev&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/github/oemof/oemof-tabular

.. |codecov| image:: https://codecov.io/github/oemof/oemof-tabular/coverage.svg?branch=dev
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof-tabular

.. |codeclimate| image:: https://codeclimate.com/github/oemof/oemof-tabular/badges/gpa.svg
   :target: https://codeclimate.com/github/oemof/oemof-tabular
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/oemof.tabular.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof.tabular

.. |commits-since| image:: https://img.shields.io/badge/dynamic/json.svg?label=%2B&url=https%3A%2F%2Fapi.github.com%2Frepos%2Foemof%2Foemof-tabular%2Fcompare%2Fv0.0.2...dev&query=%24.total_commits&colorB=blue
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-tabular/compare/v0.0.2...dev

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.tabular.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/oemof.tabular

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.tabular.svg
    :alt: Supported versions
    :target: https://pypi.org/project/oemof.tabular

.. |license| image:: https://img.shields.io/pypi/l/oemof-tabular.svg?colorB=blue
    :alt: PyPI - License
    :target: https://github.com/oemof/oemof-tabular/blob/master/LICENSE

.. end-badges

Load oemof energy systems from tabular data sources.

* Free software: BSD 3-Clause License

Installation
============

Simpy run:

::

    pip install oemof.tabular


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
