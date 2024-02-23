
Changelog
=========



Unreleased
----------


Features

* Improve reading error message `#134 <https://github.com/oemof/oemof-tabular/pull/134>`_
* Remove facade relicts `#135 <https://github.com/oemof/oemof-tabular/pull/135>`_
* Add dev install version `#147 <https://github.com/oemof/oemof-tabular/pull/147>`_

Fixes

* Remove specific dirs from flake8 & isort `#136 <https://github.com/oemof/oemof-tabular/pull/136>`_
* Update lp-files to pyomo6.7 `#148 <https://github.com/oemof/oemof-tabular/pull/148>`_
* Rework periodic value deserialization `#154 <https://github.com/oemof/oemof-tabular/pull/154>`_
* Fix oemof.solph version to v0.5.2dev1 `#157 <https://github.com/oemof/oemof-tabular/pull/157>`_
* Fix oemof.solph version to v0.5.2.dev1 `#159 <https://github.com/oemof/oemof-tabular/pull/159>`_



0.0.4 Patch Release (2023-08-31)
-----------------------------------------------------

Features

* Add PR template `#129 <https://github.com/oemof/oemof-tabular/pull/129>`_
* Add deprecation warning for python3.8 `#125 <https://github.com/oemof/oemof-tabular/pull/125>`_
* Update to oemof.solph 0.5.1 latest changes `#123 <https://github.com/oemof/oemof-tabular/pull/123>`_
* Add multi-period deserialization `#112 <https://github.com/oemof/oemof-tabular/pull/112>`_
* Add multi-period investment `#108 <https://github.com/oemof/oemof-tabular/pull/108>`_
* Make oemof.solph 0.5.1 work `#107 <https://github.com/oemof/oemof-tabular/pull/107>`_
* Split facades into submodules `#92 <https://github.com/oemof/oemof-tabular/pull/92>`_
* Add postprocessing module `#102 <https://github.com/oemof/oemof-tabular/pull/102>`_

Fixes

* Update neglected CHANGELOG `#130 <https://github.com/oemof/oemof-tabular/pull/130>`_


0.0.3 (2022-01-26)
------------------
Fixes

* Fix link by not setting constraints that limit direction `#38 <https://github.com/oemof/oemof-tabular/pull/38>`_
* Fix storage investment `#33 <https://github.com/oemof/oemof-tabular/pull/33>`_
* Link investment `#28 <https://github.com/oemof/oemof-tabular/pull/28>`_
* Variable cost `#24 <https://github.com/oemof/oemof-tabular/pull/24>`_
* Marginal cost `#23 <https://github.com/oemof/oemof-tabular/pull/23>`_

Features

* Adjust to new oemof.solph structure `#21 <https://github.com/oemof/oemof-tabular/pull/21>`_
* Allow to define custom foreign keys `#39 <https://github.com/oemof/oemof-tabular/pull/39>`_
* Add constraint tests for most facades `#35 <https://github.com/oemof/oemof-tabular/pull/35>`_, `#42 <https://github.com/oemof/oemof-tabular/pull/42>`_
* Reduce number of imported packages `#32 <https://github.com/oemof/oemof-tabular/pull/32>`_, `#49 <https://github.com/oemof/oemof-tabular/pull/49>`_
* Cleaned up the badges in README `#59 <https://github.com/oemof/oemof-tabular/pull/59>`_
* Move most CI services to github actions `#37 <https://github.com/oemof/oemof-tabular/pull/37>`_

0.0.2 (2019-07-08)
------------------

0.0.1 (2018-12-12)
------------------
* Moved the datapackage reader from core `oemof` into this package.
  That means the basic functionality of deserializing energy systems
  from datapackages has finally arrived.
* Moved `Facade` classes from `renpass` into this package.
  The `Facade` classes are designed to complement the datapackage
  reader, by enabling easy construction of energy system components from
  simple tabular data sources.
* Also moved the example datapackages from `renpass` into this package.
  These datapackages provide a good way of at least testing, that the
  datapackage reader doesn't throw errors.

0.0.0 (2018-11-23)
------------------

* First release on PyPI.
  Pretty much non functional because it only consists of the package
  boilerplate and nothing else. But this is what a version zero is for,
  IMHO.

