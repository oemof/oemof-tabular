========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

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
    :target: https://coveralls.io/r/oemof/oemof-tabular

.. |codecov| image:: https://codecov.io/github/oemof/oemof-tabular/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/oemof/oemof-tabular

.. |landscape| image:: https://landscape.io/github/oemof/oemof-tabular/master/landscape.svg?style=flat
    :target: https://landscape.io/github/oemof/oemof-tabular/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/grade/14dbd9b9c5e34f8b80e73887b5aa6e6c.svg
    :target: https://www.codacy.com/app/gnn/oemof-tabular
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/oemof/oemof-tabular/badges/gpa.svg
   :target: https://codeclimate.com/github/oemof/oemof-tabular
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/oemof.tabular.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/oemof.tabular

.. |commits-since| image:: https://img.shields.io/github/commits-since/oemof/oemof-tabular/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/oemof/oemof-tabular/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/oemof.tabular.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/oemof.tabular

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/oemof.tabular.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/oemof.tabular

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/oemof.tabular.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/oemof.tabular

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/oemof/oemof-tabular/master.svg
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/oemof/oemof-tabular/


.. end-badges

Load oemof energy systems from tabular data sources.

* Free software: BSD 3-Clause License

Installation
============

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
