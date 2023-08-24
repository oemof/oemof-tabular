=====
Usage
=====

To use oemof.tabular in a project::

	import oemof.tabular


Background
=============

The underlying concept of **oemof-tabular** is the
`oemof solph  <https://oemof.readthedocs.io/en/stable/oemof_solph.html>`_
package.
The Open Energy Modelling Framework (oemof) 	is based on a graph structure at its core.
In addition it provides an optimization model generator to construct individual
dispatch and investment models. The internal logic, used terminology and software
architecture is abstract and rather designed for model developers and
experienced modellers.

Oemof users / developers can model energy systems with different degrees
of freedom:

1. Modelling based using existing classes
2. Add own classes
3. Add own constraints based on the underlying algebraic modelling library

However, in some cases complexity of this internal logic and full functionality
is neither necessary nor suitable for model users. Therefore we provide
so called **facade classes** that provide an energy specific and reduced
access to the underlying oemof.solph functionality. More importantly theses
classes provide an interface to tabular data sources from that models can be
created easily.

.. note:: To see the implemented facades check out the :py:mod:`~oemof.tabular.facades` module.


Facades
---------------------------------

Modelling energy systems based on these classes is straightforward.
Parametrization of an energy system can either be done via python scripting or
by using the datapackage structure described below.
The documentation for the facades can be found :py:mod:`~oemof.tabular.facades`.
In addition you can check out the jupyter notebook from the tutorials
and the examples directory.

Currently we provide the following facades:

* :py:class:`~oemof.tabular.facades.Dispatchable`
* :py:class:`~oemof.tabular.facades.Volatile`
* :py:class:`~oemof.tabular.facades.Storage`
* :py:class:`~oemof.tabular.facades.Reservoir`
* :py:class:`~oemof.tabular.facades.BackpressureTurbine`
* :py:class:`~oemof.tabular.facades.ExtractionTurbine`
* :py:class:`~oemof.tabular.facades.Commodity`
* :py:class:`~oemof.tabular.facades.Conversion`
* :py:class:`~oemof.tabular.facades.Load`.
* :py:class:`~oemof.tabular.facades.Link`
* :py:class:`~oemof.tabular.facades.Excess`

These can be mixed with all oemof solph classes if your are scripting.

Datamodel and Naming Conventions
----------------------------------

Facades require specific attributes. For all facades the attribute `carrier`,
'tech' and 'type' need to be set. The type of the attribute is string,
therefore you can choose string for these. However, if you want to leverage
full postprocessing functionality we recommend using one of the types listed below

**Carriers**

* solar, wind, biomass, coal, lignite, uranium, oil, gas, hydro, waste, electricity, heat, other

**Tech types**

* st, ocgt, ccgt, ce, pv, onshore, offshore, ror, rsv, phs, ext, bp, battery

We recommend use the following naming convention for your facade names
`bus-carrier-tech-number`. For example: *DE-gas-ocgt-1*. This allows you to also
take advantage of the color map from :py:mod:`~oemof.tabular.facades` module.

.. code-block:: python

		from oemof.facades import TECH_COLOR_MAP, CARRIER_COLER_MAP

		biomass_color = CARRIER_COLER_MAP["biomass"]
		pv_color = TECH_COLOR_MAP["pv"]


Datapackage
============
To construct a model based on the datapackage the following 2
steps are required:

	1. Add the topology of the energy system based on the components and their
	**exogenous model variables** to csv-files in the datapackage format.

	2. Create a python script to construct the energy system and the model from
	that data.


We recommend a specific workflow to allow to publish your scenario
(input data, assumptions, model and results) altogether in one consistent block
based on the datapackage standard (see: Reproducible Workflows).


How to create a Datapackage
-----------------------------

We adhere to the frictionless `(tabular) datapackage standard  <https://frictionlessdata.io/specs/tabular-data-package/>`_.
On top of that structure we add our own logic. We require at least two things:

	1. A directory named *data* containing at least one sub-folder called *elements*
	(optionally it may contain a directory *sequences*, *geometries* and/or *constraints*. Of
	course you may add any other directory, data or other information.)

	2. A valid meta-data `.json` file for the datapackage

.. note:: You **MUST** provide one file with the buses called `bus.csv`!

The resulting tree of the datapackage could for example look like this:

::

    |-- datapackage
        |-- data
            |-- elements
                |-- demand.csv
                |-- generator.csv
                |-- storage.csv
                |-- bus.csv
            |-- sequences
        |-- scripts
        |-- datapackage.json

Inside the datapackage, data is stored in so called resources. For a
tabular-datapackage, these resources are CSV files. Columns of such
resources are referred to as *fields*. In this sense field names of the
resources are equivalent to parameters of the energy system elements and
sequences.

To distinguish elements and sequences these two are stored in sub-directories of
the data directory. In addition, geometrical information can be stored under
`data/geometries` in a `.geojson` format. An optional subdirectory `data/constraints`
can hold data describing global constraints.
To simplifiy the process of creating
and processing a datapackage you may
also use the funtionalities of the :py:mod:`~oemof.tabular.datapackage`

You can use functions to read and write resources (pandas.DataFrames in python).
This can also be done for sequences and geometries.

.. code-block:: python

		from oemof.tabular.datapackage import building
		...

		building.read_elements('volatile.csv')

		# manipulate data ...

		building.write_elements('volatile.csv')


To create meta-data `json` file you can use the following code:


.. code-block:: python

	from datapackage_utilities import building

	building.infer_metadata(
		package_name="my-datapackage",
		foreign_keys={
				"bus": [
					"volatile",
					"dispatchable",
					"storage",
					"heat_storage",
					"load",
					"ror",
					"reservoir",
					"phs",
					"excess",
					"boiler",
					"commodity",
				],
				"profile": ["load", "volatile", "heat_load", "ror", "reservoir"],
				"from_to_bus": ["link", "conversion", "line"],
				"chp": ["backpressure", "extraction"],
		},
		path="/home/user/datpackages/my-datapackage"
	)


Elements
--------

We recommend using one tabular data resource (i.e. one csv-file) for each
type you want to model. The fields (i.e. column names) match the attribute
names specified in the description of the facade classes.

Example for **Load**:

::

	| name      | type   | tech  |amount | profile         | bus             |
	|-----------|--------| ------|-------|-----------------|-----------------|
	| el-demand | load   | load  | 2000  | demand-profile1 | electricity-bus |
	| ...       |  ...   | ....  | ...   |     ...         |     ...         |


The corresponding meta data `schema` of the resource would look as follows:

.. code-block:: json

  "schema": {
      "fields": [
          {
              "name": "name",
              "type": "string",
          },
          {
              "name": "type",
              "type": "string",
          },
          {
              "name": "tech",
              "type": "string",
          },
          {
              "name": "amount",
              "type": "number",
          },
          {
              "name": "profile",
              "type": "string",
          },
          {
              "name": "bus",
              "type": "string",
          }
      ],
      "foreignKeys": [
            {
                "fields": "bus",
                "reference": {
                    "fields": "name",
                    "resource": "bus"
                }
            },
            {
                "fields": "profile",
                "reference": {
                    "resource": "load_profile"
                }
            }
      ],
  }

Example for **Dispatchable**:

::

	| name  | type         | capacity | capacity_cost   | bus             | marginal_cost |
	|-------|--------------|----------|-----------------|-----------------|---------------|
	| gen   | dispatchable | null     | 800             | electricity-bus | 75            |
	| ...   |     ...      |    ...   |     ...         |     ...         |  ...          |


Sequences
----------
A resource stored under
*/sequences* should at leat contain the field `timeindex` with the following
standard format ISO 8601, i.e. `YYYY-MM-DDTHH:MM:SS`.

Example:

::

	| timeindex        |  load-profile1   |  load-profile2   |
	|------------------|------------------|------------------|
	| 2016-01-01T00:00 |     0.1          |      0.05        |
	| 2016-01-01T01:00 |     0.2          |      0.1         |


The schema for resource `load_profile` stored under `sequences/load_profile.csv`
would be described as follows:

.. code-block:: json

    "schema": {
        "fields": [
            {
                "name": "timeindex",
                "type": "datetime",
            },
            {
                "name": "load-profile1",
                "type": "number",
            },
            {
                "name": "load-profile2",
                "type": "number",
            }
        ]
    }

Foreign Keys
=============

Parameter types are specified in the (json) meta-data file corresponding
to the data. In addition foreign keys can be specified to link elements
entries to elements stored in other resources (for example buses or
sequences).

To reference the *name* field of a resource with the bus elements
(bus.csv, resource name: bus) the following FK should be set in the
element resource:

.. code-block:: json

    "foreignKeys": [
      {
        "fields": "bus",
        "reference": {
          "fields": "name",
          "resource": "bus"
        }
      }
    ]

This structure can also be used to reference sequences, i.e. for the
field *profile* of a resource, the reference can be set like this:

.. code-block:: json

    "foreignKeys": [
      {
        "fields": "profile",
        "reference": {
          "resource": "generator_profile"
        }
      }
    ]

In contrast to the above example, where the foreign keys points to a
special field, in this case references are resolved by looking at the
field names in the generators-profile resource.

	.. note::

		This usage breaks with the datapackage standard and creates
		non-valid resources.**


Scripting
=========================
Currently the only way to construct a model and compute it is by using the
`oemof.solph` library. As described above, you can simply use the command line
tool on your created datapackage. However, you may also use the `facades.py`
module and write your on application.

Just read the `.json` file to create an `solph.EnergySystem` object from the
datapackage. Based on this you can create the model, compute it and process
the results.

.. code-block:: python

        from oemof.solph import EnergySystem, Model
        from renpass.facades import Load, Dispatchable, Bus

        es = EnergySystem.from_datapackage(
            'datapackage.json',
            attributemap={
                Demand: {"demand-profiles": "profile"}},
            typemap={
                'load': Load,
                'dispatchable': Dispatchable,
                'bus': Bus})

        m = Model(es)
        m.solve()


.. note::

		You may use the `attributemap` to map your your field names to facade
		class attributes. In addition you may also use different names for types in your
		datapackage and map those to the facade classes (use `typemap` attribute for
		this)

Postprocessing
--------------
After solving the energysystem model, results can be calculated using the
:py:mod:`~oemof.tabular.postprocessing` module. The postprocessing module itself consists of four modules:
- :py:mod:`~oemof.tabular.postprocessing.core` holds base classes for postprocessing
- :py:mod:`~oemof.tabular.postprocessing.calculations` holds predefined calculations
- :py:mod:`~oemof.tabular.postprocessing.helper` holds helper functions which are used in calculations
- :py:mod:`~oemof.tabular.postprocessing.naming` holds functions for naming results and adding additional information

The standard way of using the postprocessing module is to initiate the
:py:class:`~oemof.tabular.postprocessing.core.Calculator` class from
:py:mod:`~oemof.tabular.postprocessing.core` module with parameters and results from an optimized :py:mod:`~oemof.solph` `Energysystem`.
Afterwards, calculations can be performed by either using predefined calculations from :py:mod:`~oemof.tabular.postprocessing.calculations` or
by self-defined calculations inherited from :py:class:`~oemof.tabular.postprocessing.core.Calculation` class in
:py:mod:`~oemof.tabular.postprocessing.core`.

See the following example on how to use the :py:mod:`~oemof.tabular.postprocessing` module:

.. code-block:: python

    from oemoflex.postprocessing import core, calculations

    calculator = core.Calculator(es.params, es.results)

    aggregated_flows = calculations.AggregatedFlows(calculator).result
    storage_losses = calculations.StorageLosses(calculator).result
    transmission_losses = calculations.TransmissionLosses(calculator).result
    invested_capacity = calculations.InvestedCapacity(calculator).result
    invested_storage_capacity = calculations.InvestedStorageCapacity(calculator).result
    invested_capacity_costs = calculations.InvestedCapacityCosts(calculator).result
    invested_storage_capacity_costs = calculations.InvestedStorageCapacityCosts(calculator).result
    summed_carrier_costs = calculations.SummedCarrierCosts(calculator).result
    summed_marginal_costs = calculations.SummedMarginalCosts(calculator).result
    total_system_costs = calculations.TotalSystemCosts(calculator).result


Reproducible Workflows
=======================

To get reproducible results we recommend setting up a folder structure
as follows:

::

	|-- model
		|-- environment
			|--requirements.txt
		|-- raw-data
		|-- scenarios
			|--scenario1.toml
			|--scenatio2.toml
			|-- ...
		|-- scripts
			|--create_input_data.py
			|--compute.py
			|-- ...
		|-- results
			|--scenario1
				|--input
				|--output
			 |-- scenario2
				|--input
				|--ouput


The `raw-data` directory contains all input data files required to build the
input datapckages for your modelling. This data can also be downloaded
from an additional repository which adheres to FAIR principles, like zenodo.
If you provide raw data, make sure the license is compatiple with other data
in your repository. The `scenarios` directory allows you
to specify different scenarios and describe them in a basic way via config files.
The `toml` standard is used by oemof-tabular, howerver you may also use `yaml`,
`json`, etc..
The scripts inside the `scripts` directory will build input data for your
scenarios from the `.toml` files and the raw-data. This data will be in the
format
that oemof-tabular datapackage reader can understand. In addition the script
to compute the models and postprocess results are stored there.

Of course the structure may be adapted to your needs. However you should
provide all this data when publishing results.

Debugging
=============

Debugging can sometimes be tricky, here are some things you might want to
consider:

Components do not end up in the model
---------------------------------------

	* Does the data resource (i.e. csv-file) for your components exist in the
	  `datapackage.json` file
	* Did you set the `attributemap` and `typemap` arguments of the
	  `EnergySystem.from_datapackge()` method correctly? Make sure all classes
	  with their types are present.

Errors when reading a datapackage
-----------------------------------------

	* Does the column order match the order of fields in the (tabular) data
	  resource?
	* Does the type match the types in of the columns (i.e. for integer, obviously
	  only integer values should be in the respective column)


If you encounter this error message when reading a datapackage, you most likely
provided `output_parameters` that are of type object for a tabular resource.
However, there will be emtpy entries in the field of your `output_parameters`.


	.. code-block:: python

		...
		TypeError: type object argument after ** must be a mapping, not NoneType


	.. note::

		If your column / field in a tabular resource is of a specific type, make
		sure every entry in thies column has this type! For example numeric and
		empty entries in combination will yield string as a type and not numeric!


OEMOF related errors
--------------------------

If you encounter errors from oemof, the objects are not instantiated correctly
which may happen if something of the following is wrong in your metadata file.


* Errors regarding the non-int type like this one:

	.. code-block:: python

	  ...
	  self.flows[o, i].nominal_value)
	  TypeError: can't multiply sequence by non-int of type 'float'


	Check your type(s) in the `datapackage.json` file. If meta-data are inferred types
	might be string instead of number or integer which most likely causes such an error.

* Profiles for volatile and load components

	.. code-block:: python

	  ...
	  ValueError: Cannot fix flow value to None.
	  Please set the actual_value attribute of the flow


	This error is likely to occur if your foreign keys are set correctly but
	the name in the field `profile` of your `volatilel.csv` resource does not match
	any name inside the `volatile_profile.csv` file, i.e. the profile is not found
	where it is looked for.


	Another possible source of error might be the missing values in your
	sequences files. Check these files for NaNs.



Solver and pyomo related errors
-------------------------------

If you encounter an error for writing a lp-file, you might want to check if
your foreign-keys are set correctly. In particular for resources with fk's for
sequences. If this is missing, you will get unsupported operation string and
numeric. This will unfortunately only happen on the pyomo level currently.

Also the following error might occure:

	.. code-block:: python

		...
		File "/home/admin/projects/oemof-tabular/venv/lib/python3.6/site-packages/pyomo/repn/plugins/cpxlp.py", line 849, in _print_model_LP
	 	% (_no_negative_zero(vardata_ub)))
		TypeError: must be real number, not str

This message may indicate that fields in your datapackage that should be numeric
are actually of type string. While pyomo seems sometimes still to be fine with
this, solvers are not. Here also check your meta data types and the data. Most
likely this happens if meta data is inferred from the data and fields with numeric
values are left empty which will yield a string type for this field.
