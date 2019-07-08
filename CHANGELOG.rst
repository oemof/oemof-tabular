
Changelog
=========

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

