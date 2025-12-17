========
Overview
========

.. start-badges

|version| |commits-since| |supported-versions| |license|

|docs| |wheel|


.. |docs| image:: https://readthedocs.org/projects/oemof-datapackage/badge/?style=flat
    :target: https://readthedocs.org/projects/oemof-datapackage
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/oemof.datapackage.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/oemof.datapackage

.. |commits-since| image:: https://img.shields.io/badge/dynamic/json.svg?label=%2B&url=https%3A%2F%2Fapi.github.com%2Frepos%2Foemof%2Foemof-datapackage%2Fcompare%2Fv0.0.5...dev&query=%24.total_commits&colorB=blue
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-datapackage/compare/v0.0.5...dev

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.datapackage.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/oemof.datapackage

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.datapackage.svg
    :alt: Supported versions
    :target: https://pypi.org/project/oemof.datapackage

.. |license| image:: https://img.shields.io/pypi/l/oemof-datapackage.svg?colorB=blue
    :alt: PyPI - License
    :target: https://github.com/oemof/oemof-datapackage/blob/master/LICENSE

.. end-badges

Load oemof energy systems from datapackage data sources.

We plan to use the datapackage idea for oemof-solph without being bound to the internal facade structure of oemof-tabular.

If we do this within the tabular structure, there is a risk of breaking the package for others. That is why we decided to fork the project first and then consider later how we can bring the results back together. We don't know how many people use tabular's internal classes and why. There are now more options in oemof-solph and other repositories exist that offer derived components. So the gap that tabular once filled no longer exists to the same extent. But the datapackage itself is a great idea that should be accessable without the tabular structure.

* Free software: BSD 3-Clause License

Installation
============

Simpy run:

::

    pip install oemof.datapackage


Documentation
=============


https://oemof-datapackage.readthedocs.io/


Development
===========

Please activate pre-commit hooks in order to follow our coding styles:

::

    pip install pre-commit
    pre-commit install

To run the all tests run:

::

    pytest


..    tox

.. Note, to combine the coverage data from all the tox environments run:

.. .. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
