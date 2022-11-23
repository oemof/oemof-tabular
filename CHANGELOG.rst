
Changelog
=========

0.0.3 (2022-11-17)
------------------
Fixes
#####

* Fix link by not setting constraints that limit direction #38
* Storage investment #33
* Link investment #28
* Variable cost #24
* Marginal cost #23

Features
########

* Adjust to new oemof.solph structure #21
* Allow to define custom foreign keys #39
* Add constraint tests for most facades #35 #42
* Reduce number of imported packages #32 #49
* Cleaned up the badges in README #59
* Move most CI services to github actions # 37

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

