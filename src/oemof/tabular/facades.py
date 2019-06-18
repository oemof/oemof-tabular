# -*- coding: utf-8 -*-

""" Facade's are classes providing a simplified view on more complex classes.

More specifically, the `Facade`s in this module act as simplified, energy
specific  wrappers around `oemof`'s and `oemof.solph`'s more abstract and
complex classes. The idea is to be able to instantiate a `Facade` using keyword
arguments, whose value are derived from simple, tabular data sources. Under the
hood the `Facade` then uses these arguments to construct an `oemof` or
`oemof.solph` component and sets it up to be easily used in an `EnergySystem`.

**Note** The mathematical notation is as follows:

* Optimization variables (endogenous variables) are denoted by :math:`x`
* Optimization parameters (exogenous variables) are denoted by :math:`c`
* The set of timesteps :math:`T` describes all timesteps of the optimization problem

SPDX-License-Identifier: BSD-3-Clause
"""
from oemof.network import Node
from oemof.solph import Bus, Flow, Investment, Sink, Source, Transformer
from oemof.solph.components import ExtractionTurbineCHP, GenericStorage
from oemof.solph.custom import ElectricalBus, ElectricalLine, Link
from oemof.solph.plumbing import sequence


class Facade(Node):
    """
    Parameters
    ----------
    _facade_requires_ : list of str
        A list of required attributes. The constructor checks whether these are
        present as keywort arguments or whether they are already present on
        self (which means they have been set by constructors of subclasses) and
        raises an error if he doesn't find them.
    """

    def __init__(self, *args, **kwargs):
        """
        """

        self.mapped_type = type(self)

        self.type = kwargs.get("type")

        required = kwargs.pop("_facade_requires_", [])

        super().__init__(*args, **kwargs)
        self.subnodes = []
        for r in required:
            if r in kwargs:
                setattr(self, r, kwargs[r])
            elif not hasattr(self, r):
                raise AttributeError(
                    (
                        "Missing required attribute `{}` for `{}` "
                        "object with name/label `{!r}`."
                    ).format(r, type(self).__name__, self.label)
                )

    def _nominal_value(self):
        """ Returns None if self.expandable ist True otherwise it returns
        the capacity
        """
        if self.expandable == True:
            return None

        else:
            return self.capacity

    def _investment(self):
        if self.expandable == True:
            if self.capacity_cost is None:
                msg = (
                    "If you set `expandable`to True you need to set "
                    "attribute `capacity_cost` of component {}!"
                )
                raise ValueError(msg.format(self.label))
            else:
                if isinstance(self, GenericStorage):
                    if self.storage_capacity_cost is not None:
                        self.investment = Investment(
                            ep_costs=self.storage_capacity_cost,
                            maximum=getattr(
                                self,
                                "storage_capacity_potential",
                                float("+inf")),
                            minimum=getattr(
                                self,
                                "minimum_storage_capacity",
                                0),
                            existing=getattr(self, "storage_capacity", 0)
                        )
                    else:
                        self.investment = Investment()
                else:
                    self.investment = Investment(
                        ep_costs=self.capacity_cost,
                        maximum=getattr(
                            self, "capacity_potential", float("+inf")
                        ),
                        existing=getattr(self, "capacity", 0)
                    )
        else:
            self.investment = None

        return self.investment

    def update(self):
        self.build_solph_components()


class Reservoir(GenericStorage, Facade):
    """ A Reservoir storage unit, that is initially half full.

    Note that the investment option is not available for this facade at
    the current development state.

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total storage capacity of the storage (e.g. in MWh)
    capacity: numeric
        Installed production capacity of the turbine installed at the
        reservoir
    efficiency: numeric
        Efficiency of the turbine converting inflow to electricity
        production, default: 1
    profile: array-like
        Absolute inflow profile of inflow into the storage
    input_parameters: dict
        Dictionary to specifiy parameters on the input edge. You can use
        all keys that are available for the  oemof.solph.network.Flow class.
    output_parameters: dict
        see: input_parameters


    The reservoir is modelled as a storage with a constant inflow:

    .. math::

        x^{level}(t) = \
        x^{level}(t-1) \cdot (1 - c^{loss\_rate}(t)) \
        + x^{profile}(t) - \\frac{x^{flow, out}(t)}{c^{efficiency}(t)} \
        \\qquad \\forall t \in T

    .. math::
        x^{level}(0) = 0.5 \cdot c^{capacity}

    The inflow is bounded by the exogenous inflow profile. Thus if the inflow
    exceeds the maximum capacity of the storage, spillage is possible by setting
    :math:`x^{profile}(t)` to lower values.

    .. math::
        0 \leq x^{profile}(t) \leq c^{profile}(t) \\qquad \\forall t \\in T


    The spillage of the reservoir is therefore defined by:
    :math:`c^{profile}(t) - x^{profile}(t)`.

    Note
    ----
    As the Reservoir is a sub-class of `oemof.solph.GenericStorage` you also
    pass all arguments of this class.


    Examples
    --------
    Basic usage examples of the GenericStorage with a random selection of
    attributes. See the Flow class for all Flow attributes.

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_reservoir = Reservoir(
    ...     label='my_reservoir',
    ...     bus=my_bus,
    ...     carrier='water',
    ...     tech='reservoir',
    ...     storage_capacity=1000,
    ...     capacity=50,
    ...     profile=[1, 2, 6],
    ...     loss_rate=0.01,
    ...     initial_storage_level=0,
    ...     max_storage_level = 0.9,
    ...     efficiency=0.93)

    """

    def __init__(self, *args, **kwargs):

        kwargs.update(
            {
                "_facade_requires_": [
                    "bus",
                    "carrier",
                    "tech",
                    "profile",
                    "efficiency",
                ]
            }
        )
        super().__init__(*args, **kwargs)

        self.storage_capacity = kwargs.get("storage_capacity")

        self.capacity = kwargs.get("capacity")

        self.efficiency = kwargs.get("efficiency", 1)

        self.profile = kwargs.get("profile")

        self.input_parameters = kwargs.get("input_parameters", {})

        self.output_parameters = kwargs.get("output_parameters", {})

        self.expandable = bool(kwargs.get("expandable", False))

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        self.nominal_storage_capacity = self.storage_capacity

        self.outflow_conversion_factor = sequence(self.efficiency)

        if self.expandable:
            raise NotImplementedError(
                "Investment for reservoir class is not implemented."
            )

        inflow = Source(
            label=self.label + "-inflow",
            outputs={
                self: Flow(nominal_value=1, max=self.profile, fixed=False)
            },
        )

        self.outputs.update(
            {
                self.bus: Flow(
                    nominal_value=self.capacity,
                    **self.output_parameters
                )
            }
        )

        self.subnodes = (inflow,)


class Dispatchable(Source, Facade):
    """ Dispatchable element with one output for example a gas-turbine

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the unit is connected to with its output
    capacity: numeric
        The installed power of the generator (e.g. in MW). If not set the
        capacity will be optimized (s. also `capacity_cost` argument)
    profile: array-like (optional)
        Profile of the output such that profile[t] * installed capacity
        yields the upper bound for timestep t
    marginal_cost: numeric
        Marginal cost for one unit of produced output, i.e. for a powerplant:
        mc = fuel_cost + co2_cost + ... (in Euro / MWh) if timestep length is
        one hour. Default: 0
    capacity_cost: numeric (optional)
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.
    output_paramerters: dict (optional)
        Parameters to set on the output edge of the component (see. oemof.solph
        Edge/Flow class for possible arguments)
    capacity_potential: numeric
        Max install capacity if capacity is to be expanded


    The mathematical representations for this components are dependent on the
    user defined attributes. If the capacity is fixed before (**dispatch mode**)
    the following equation holds:

    .. math::

        x^{flow}(t) \leq c^{capacity} \cdot c^{profile}(t) \\qquad \\forall t \in T

    Where :math:`x^{flow}` denotes the production (endogenous variable)
    of the dispatchable object to the bus.

    If `expandable` is set to `True` (**investment mode**), the equation
    changes slightly:

    .. math::

        x^{flow}(t) \leq (x^{capacity} + \
        c^{capacity})  \cdot c^{profile}(t) \\qquad \\forall t \in T

    Where the bounded endogenous variable of the volatile component is added:

    ..  math::

            x^{capacity} \leq c^{capacity\_potential}

    **Ojective expression** for operation:

    .. math::

        x^{opex} = \sum_t x^{flow}(t) \cdot c^{marginal\_cost}(t)

    For constraints set through `output_parameters` see oemof.solph.Flow class.


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_dispatchable = Dispatchable(
    ...     label='ccgt',
    ...     bus=my_bus,
    ...     carrier='gas',
    ...     tech='ccgt',
    ...     capacity=1000,
    ...     marginal_cost=10,
    ...     output_parameters={
    ...         'max': 0.9})

    """

    def __init__(self, *args, **kwargs):
        kwargs.update({"_facade_requires_": ["bus", "carrier", "tech"]})
        super().__init__(*args, **kwargs)

        self.profile = kwargs.get("profile", 1)

        self.capacity = kwargs.get("capacity")

        self.capacity_potential = kwargs.get("capacity_potential")

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.expandable = bool(kwargs.get("expandable", False))

        self.output_parameters = kwargs.get("output_parameters", {})

        self.build_solph_components()

    def build_solph_components(self):
        """
        """

        f = Flow(
            nominal_value=self._nominal_value(),
            variable_costs=self.marginal_cost,
            max=self.profile,
            investment=self._investment(),
            **self.output_parameters
        )

        self.outputs.update({self.bus: f})


class Volatile(Source, Facade):
    """Volatile element with one output. This class can be used to model
    PV oder Wind power plants.


    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the generator is connected to
    capacity: numeric
        The installed power of the unit (e.g. in MW).
    profile: array-like
        Profile of the output such that profile[t] * capacity yields output
        for timestep t
    marginal_cost: numeric
        Marginal cost for one unit of produced output, i.e. for a powerplant:
        mc = fuel_cost + co2_cost + ... (in Euro / MWh) if timestep length is
        one hour.
    capacity_cost: numeric (optional)
        Investment costs per unit of capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        generators capacity.
    output_paramerters: dict (optional)
        Parameters to set on the output edge of the component (see. oemof.solph
        Edge/Flow class for possible arguments)
    capacity_potential: numeric
        Max install capacity if investment
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.
    fixed: boolean
        If False, the output may be curtailed when optimizing dispatch.
        Default: True


    The mathematical representations for this components are dependent on the
    user defined attributes. If the capacity is fixed before (**dispatch mode**)
    the following equation holds:

    .. math::

        x^{flow}(t) = c^{capacity} \cdot c^{profile}(t) \\qquad \\forall t \in T

    Where :math:`x_{volatile}^{flow}` denotes the production (endogenous variable)
    of the volatile object to the bus.

    If `expandable` is set to `True` (**investment mode**), the equation
    changes slightly:

    .. math::

        x^{flow}(t) = (x^{capacity} + c^{capacity}) \
         \cdot c^{profile}(t)  \\qquad \\forall t \in T

    Where the bounded endogenous variable of the volatile component is added:

    ..  math::

            x_{volatile}^{capacity} \leq c_{volatile}^{capacity\_potential}

    **Ojective expression** for operation:

    .. math::

        x^{opex} = \sum_t (x^{flow}(t) \cdot c^{marginal\_cost}(t))

    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_volatile = Volatile(
    ...     label='wind',
    ...     bus=my_bus,
    ...     carrier='wind',
    ...     tech='onshore',
    ...     capacity_cost=150,
    ...     profile=[0.25, 0.1, 0.3])

    """

    def __init__(self, *args, **kwargs):
        kwargs.update({"_facade_requires_": ["bus", "carrier", "tech",
                                             "profile"]})
        super().__init__(*args, **kwargs)

        self.profile = kwargs.get("profile")

        self.capacity = kwargs.get("capacity")

        self.capacity_potential = kwargs.get("capacity_potential")

        self.expandable = bool(kwargs.get("expandable", False))

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.output_parameters = kwargs.get("output_parameters", {})

        self.fixed = bool(kwargs.get('fixed', True))

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        f = Flow(
            nominal_value=self._nominal_value(),
            variable_costs=self.marginal_cost,
            actual_value=self.profile,
            investment=self._investment(),
            fixed=self.fixed,
            **self.output_parameters
        )

        self.outputs.update({self.bus: f})


class ExtractionTurbine(ExtractionTurbineCHP, Facade):
    """ Combined Heat and Power (extraction) unit with one input and
    two outputs.

    Parameters
    ----------
    electricity_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        electrical output
    heat_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        thermal output
    fuel_bus:  oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        input
    carrier_cost: numeric
        Cost per unit of used input carrier
    capacity: numeric
        The electrical capacity of the chp unit (e.g. in MW) in full extraction
        mode.
    electric_efficiency:
        Electrical efficiency of the chp unit in full backpressure mode
    thermal_efficiency:
        Thermal efficiency of the chp unit in full backpressure mode
    condensing_efficiency:
        Electrical efficiency if turbine operates in full extraction mode
    marginal_cost: numeric
        Marginal cost for one unit of produced electrical output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour.
    capacity_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.


    The mathematical description is derived from the oemof base class
    `ExtractionTurbineCHP <https://oemof.readthedocs.io/en/stable/oemof_solph.html#extractionturbinechp-component>`_ :

    .. math::
        x^{flow, carrier} = \
        \\frac{x^{flow, electricity}(t) + x^{flow, heat}(t) \cdot c^{beta}(t)}{c^{condensing\_efficiency}(t)} \
        \\qquad \\forall t \\in T

    .. math::
        x^{flow, electricity}(t)  \geq  x^{flow, thermal}(t) \cdot \
        \\frac{c^{electrical\_efficiency}(t)}{c^{thermal\_efficiency}(t)} \
        \\qquad \\forall t \\in T

    where :math:`c^{beta}` is defined as:

     .. math::
        c^{beta}(t) = \\frac{c^{condensing\_efficiency}(t) - \
        c^{electrical\_efficiency(t)}}{c^{thermal\_efficiency}(t)} \
        \\qquad \\forall t \\in T

    **Ojective expression** for operation includes marginal cost and/or
    carrier costs:

        .. math::

            x^{opex} = \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t) \
            + x^{flow, carrier} \cdot c^{carrier\_cost}(t))


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_elec_bus = solph.Bus('my_elec_bus')
    >>> my_fuel_bus = solph.Bus('my_fuel_bus')
    >>> my_heat_bus = solph.Bus('my_heat_bus')
    >>> my_extraction = ExtractionTurbine(
    ...     label='extraction',
    ...     carrier='gas',
    ...     tech='ext',
    ...     electricity_bus=my_elec_bus,
    ...     heat_bus=my_heat_bus,
    ...     fuel_bus=my_fuel_bus,
    ...     capacity=1000,
    ...     condensing_efficiency=[0.5, 0.51, 0.55],
    ...     electric_efficiency=0.4,
    ...     thermal_efficiency=0.35)

    """

    def __init__(self, *args, **kwargs):
        kwargs.update(
            {
                "_facade_requires_": [
                    "fuel_bus",
                    "carrier",
                    "tech",
                    "electricity_bus",
                    "heat_bus",
                    "thermal_efficiency",
                    "electric_efficiency",
                    "condensing_efficiency",
                ]
            }
        )
        super().__init__(
            conversion_factor_full_condensation={}, *args, **kwargs
        )

        self.fuel_bus = kwargs.get("fuel_bus")

        self.electricity_bus = kwargs.get("electricity_bus")

        self.heat_bus = kwargs.get("heat_bus")

        self.carrier = kwargs.get("carrier")

        self.carrier_cost = kwargs.get("carrier_cost", 0)

        self.capacity = kwargs.get("capacity")

        self.condensing_efficiency = sequence(self.condensing_efficiency)

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.expandable = bool(kwargs.get("expandable", False))

        self.input_parameters = kwargs.get("input_parameters", {})

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        self.conversion_factors.update(
            {
                self.fuel_bus: sequence(1),
                self.electricity_bus: sequence(self.electric_efficiency),
                self.heat_bus: sequence(self.thermal_efficiency),
            }
        )

        self.inputs.update(
            {
                self.fuel_bus: Flow(
                    variable_cost=self.carrier_cost, **self.input_parameters
                )
            }
        )

        self.outputs.update(
            {
                self.electricity_bus: Flow(
                    nominal_value=self._nominal_value(),
                    variable_costs=self.marginal_cost,
                    investment=self._investment(),
                ),
                self.heat_bus: Flow(),
            }
        )

        self.conversion_factor_full_condensation.update(
            {self.electricity_bus: self.condensing_efficiency}
        )


class BackpressureTurbine(Transformer, Facade):
    """ Combined Heat and Power (backpressure) unit with one input and
    two outputs.

    Parameters
    ----------
    electricity_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        electrical output
    heat_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        thermal output
    fuel_bus: oemof.solph.Bus
        An oemof bus instance where the chp unit is connected to with its
        input
    carrier_cost: numeric
        Input carrier cost of the backpressure unit, Default: 0
    capacity: numeric
        The electrical capacity of the chp unit (e.g. in MW).
    electric_efficiency:
        Electrical efficiency of the chp unit
    thermal_efficiency:
        Thermal efficiency of the chp unit
    marginal_cost: numeric
        Marginal cost for one unit of produced electrical output
        E.g. for a powerplant:
        marginal cost =fuel cost + operational cost + co2 cost (in Euro / MWh)
        if timestep length is one hour. Default: 0
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.
    capacity_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.


    Backpressure turbine power plants are modelled with a constant relation
    between heat and electrical output (power to heat coefficient).

    .. math::

        x^{flow, carrier}(t) = \
        \\frac{x^{flow, electricity}(t) + x^{flow, heat}(t)}{c^{thermal\:efficiency}(t) + c^{electrical\:efficiency}(t)} \
        \\qquad \\forall t \\in T

    .. math::

        \\frac{x^{flow, electricity}(t)}{x_{flow, thermal}(t)} = \
        \\frac{c^{electrical\:efficiency}(t)}{c^{thermal\:efficiency}(t)} \
        \\qquad \\forall t \\in T

    **Ojective expression** for operation includes marginal cost and/or
    carrier costs:

        .. math::

            x^{opex} = \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t) \
            + x^{flow, carrier} \cdot c^{carrier\_cost}(t))

    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_elec_bus = solph.Bus('my_elec_bus')
    >>> my_fuel_bus = solph.Bus('my_fuel_bus')
    >>> my_heat_bus = solph.Bus('my_heat_bus')
    >>> my_backpressure = BackpressureTurbine(
    ...     label='backpressure',
    ...     carrier='gas',
    ...     tech='bp',
    ...     fuel_bus=my_fuel_bus,
    ...     heat_bus=my_heat_bus,
    ...     electricity_bus=my_elec_bus,
    ...     capacity_cost=50,
    ...     carrier_cost=0.6,
    ...     electric_efficiency=0.4,
    ...     thermal_efficiency=0.35)


    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            _facade_requires_=[
                "carrier",
                "tech",
                "electricity_bus",
                "heat_bus",
                "fuel_bus",
                "thermal_efficiency",
                "electric_efficiency",
            ],
            *args,
            **kwargs
        )

        self.electricity_bus = kwargs.get("electricity_bus")

        self.heat_bus = kwargs.get("heat_bus")

        self.fuel_bus = kwargs.get("fuel_bus")

        self.capacity = kwargs.get("capacity")

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.carrier_cost = kwargs.get("carrier_cost", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.expandable = bool(kwargs.get("expandable", False))

        self.input_parameters = kwargs.get("input_parameters", {})

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        self.conversion_factors.update(
            {
                self.fuel_bus: sequence(1),
                self.electricity_bus: sequence(self.electric_efficiency),
                self.heat_bus: sequence(self.thermal_efficiency),
            }
        )

        self.inputs.update(
            {
                self.fuel_bus: Flow(
                    variable_costs=self.carrier_cost, **self.input_parameters
                )
            }
        )

        self.outputs.update(
            {
                self.electricity_bus: Flow(
                    nominal_value=self._nominal_value(),
                    investment=self._investment()
                ),
                self.heat_bus: Flow(),
            }
        )


class Conversion(Transformer, Facade):
    """ Conversion unit with one input and one output.

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its output.
    capacity: numeric
        The conversion capacity (output side) of the unit.
    efficiency: numeric
        Efficiency of the conversion unit (0 <= efficiency <= 1). Default: 1
    marginal_cost: numeric
        Marginal cost for one unit of produced output. Default: 0
    carrier_cost: numeric
        Carrier cost for one unit of used input. Default: 0
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        conversion output capacity.
    expandable: boolean or numeric (binary)
        True, if capacity can be expanded within optimization. Default: False.
    capacity_potential: numeric
        Maximum invest capacity in unit of output capacity.
    input_parameters: dict (optional)
        Set parameters on the input edge of the conversion unit
        (see oemof.solph for more information on possible parameters)
    ouput_parameters: dict (optional)
        Set parameters on the output edge of the conversion unit
         (see oemof.solph for more information on possible parameters)


    .. math::
        x^{flow, from}(t) \cdot c^{efficiency}(t) = x^{flow, to}(t) \
        \\qquad \\forall t \\in T

    **Ojective expression** for operation includes marginal cost and/or
    carrier costs:

        .. math::

            x^{opex} =  \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t) \
            + x^{flow, carrier} \cdot c^{carrier\_cost}(t))


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_biomass_bus = solph.Bus('my_biomass_bus')
    >>> my_heat_bus = solph.Bus('my_heat_bus')
    >>> my_conversion = Conversion(
    ...     label='biomass_plant',
    ...     carrier='biomass',
    ...     tech='st',
    ...     from_bus=my_biomass_bus,
    ...     to_bus=my_heat_bus,
    ...     capacity=100,
    ...     efficiency=0.4)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            _facade_requires_=["from_bus", "to_bus", "carrier", "tech"],
            *args,
            **kwargs
        )

        self.capacity = kwargs.get("capacity")

        self.efficiency = kwargs.get("efficiency", 1)

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.carrier_cost = kwargs.get("carrier_cost", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.expandable = bool(kwargs.get("expandable", False))

        self.capacity_potential = kwargs.get("capacity_potential")

        self.input_parameters = kwargs.get("input_parameters", {})

        self.output_parameters = kwargs.get("output_parameters", {})

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        self.conversion_factors.update(
            {
                self.from_bus: sequence(1),
                self.to_bus: sequence(self.efficiency),
            }
        )

        self.inputs.update({self.from_bus: Flow(
            variable_costs=self.carrier_cost, **self.input_parameters)})

        self.outputs.update(
            {
                self.to_bus: Flow(
                    nominal_value=self._nominal_value(),
                    variable_costs=self.marginal_cost,
                    investment=self._investment(),
                    **self.output_parameters
                )
            }
        )


class Load(Sink, Facade):
    """ Load object with one input

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the demand is connected to.
    amount: numeric
        The total amount for the timehorzion (e.g. in MWh)
    profile: array-like
        Load profile with normed values such that `profile[t] * amount`
        yields the load in timestep t (e.g. in MWh)
    marginal_utility: numeric
        Marginal utility in for example Euro / MWh
    fixed: boolean
        True, if demand should be inelastic (Default: True)
    input_parameters: dict (optional)



    .. math::
        x^{flow}(t) = c^{amount}(t)  \cdot x^{flow}(t) \qquad \\forall t \\in T


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_load = Load(
    ...     label='load',
    ...     carrier='electricity',
    ...     bus=my_bus,
    ...     amount=100,
    ...     profile=[0.3, 0.2, 0.5])
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            _facade_requires_=["bus", "amount", "profile"], *args, **kwargs
        )

        self.amount = kwargs.get("amount")

        self.profile = kwargs.get("profile")

        self.input_parameters = kwargs.get("input_parameters", {})

        self.marginal_utility = kwargs.get("marginal_utility", 0)

        self.fixed = kwargs.get("fixed", True)

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        self.inputs.update(
            {
                self.bus: Flow(
                    nominal_value=self.amount,
                    actual_value=self.profile,
                    fixed=self.fixed,
                    variable_cost=self.marginal_utility,
                    **self.input_parameters
                )
            }
        )


class Storage(GenericStorage, Facade):
    """ Storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    capacity: numeric
        Maximum production capacity (e.g. in MW)
    efficiency: numeric
        Efficiency of charging and discharging process: Default: 1
    storage_capacity_cost: numeric
        Investment costs for the storage unit e.g in €/MWh-capacity
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.
    storage_capacity_potential: numeric
        Potential of the investment for storage capacity in MWh
    capacity_potential: numeric
        Potential of the investment for capacity in MW
    input_parameters: dict (optional)
        Set parameters on the input edge of the storage (see oemof.solph for
        more information on possible parameters)
    ouput_parameters: dict (optional)
        Set parameters on the output edge of the storage (see oemof.solph for
        more information on possible parameters)


    Intertemporal energy balance of the storage:

    .. math::

        x^{level}(t) = \
        x^{level}(t-1) \cdot (1 - c^{loss\_rate}) \
        + \\sqrt{c^{efficiency}(t)}  x^{flow, in}(t) \
        - \\frac{x^{flow, out}(t)}{\\sqrt{c^{efficiency}(t)}} \
        \\qquad \\forall t \in T

    .. math::
        x^{level}(0) = 0.5 \cdot c^{capacity}

    The **expression** added to the cost minimizing objective funtion
    for the operation is given as:

    .. math::

        x^{opex} = \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t))


    Examples
    ---------

    >>> import pandas as pd
    >>> from oemof import solph
    >>> from oemof.tabular import facades as fc
    >>> my_bus = solph.Bus('my_bus')
    >>> es = solph.EnergySystem(
    ...    timeindex=pd.date_range('2019', periods=3, freq='H'))
    >>> es.add(my_bus)
    >>> es.add(
    ...    fc.Storage(
    ...        label="storage",
    ...        bus=my_bus,
    ...        carrier="lithium",
    ...        tech="battery",
    ...        storage_capacity_cost=10,
    ...        invest_relation_output_capacity=1/6, # oemof.solph
    ...        marginal_cost=5,
    ...        balanced=True, # oemof.solph argument
    ...        initial_storage_level=1, # oemof.solph argument
    ...        max_storage_level=[0.9, 0.95, 0.8])) # oemof.solph argument

    """

    def __init__(self, *args, **kwargs):

        super().__init__(
            _facade_requires_=["bus", "carrier", "tech"], *args, **kwargs
        )

        self.storage_capacity = kwargs.get("storage_capacity", 0)

        self.capacity = kwargs.get("capacity", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.storage_capacity_cost = kwargs.get("storage_capacity_cost")

        self.storage_capacity_potential = kwargs.get(
            "storage_capacity_potential", float("+inf"))

        self.capacity_potential = kwargs.get(
            "capacity_potential", float("+inf"))

        self.expandable = bool(kwargs.get("expandable", False))

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.efficiency = kwargs.get("efficiency", 1)

        self.input_parameters = kwargs.get("input_parameters", {})

        self.output_parameters = kwargs.get("output_parameters", {})

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        self.nominal_storage_capacity = self.storage_capacity

        self.inflow_conversion_factor = sequence(self.efficiency)

        self.outflow_conversion_factor = sequence(self.efficiency)

        # make it investment but don't set costs (set below for flow (power))
        self.investment = self._investment()

        if self.investment:
            self.invest_relation_input_output = 1

            for attr in [
                "invest_relation_input_output",
            ]:
                if getattr(self, attr) is None:
                    raise AttributeError(
                        (
                            "You need to set attr " "`{}` " "for component {}"
                        ).format(attr, self.label)
                    )

            # set capacity costs at one of the flows
            fi = Flow(
                investment=Investment(
                    ep_costs=self.capacity_cost,
                    maximum=self.capacity_potential,
                    existing=self.capacity
                ),
                **self.input_parameters
            )
            # set investment, but no costs (as relation input / output = 1)
            fo = Flow(
                investment=Investment(),
                variable_costs=self.marginal_cost,
                **self.output_parameters
            )
            # required for correct grouping in oemof.solph.components
            self._invest_group = True
        else:
            fi = Flow(
                nominal_value=self._nominal_value(),
                **self.input_parameters)
            fo = Flow(
                nominal_value=self._nominal_value(),
                variable_costs=self.marginal_cost,
                **self.output_parameters
            )

        self.inputs.update({self.bus: fi})

        self.outputs.update({self.bus: fo})

        self._set_flows()


class Link(Link, Facade):
    """ Bi-direction link for two buses (e.g. to model transshipment)

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the link unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the link unit is connected to with
        its output.
    capacity: numeric
        The maximal capacity (output side each) of the unit. If not set, attr
        `capacity_cost` needs to be set.
    loss:
        Relative loss through the link (default: 0)
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        chp capacity.
    marginal_cost: numeric
        Cost per unit Transport in each timestep. Default: 0
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.


    Note
    -----
    Assigning a small value like 0.00001 to `marginal_cost`  may force unique
    solution of optimization problem.

    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_elec_bus_1 = solph.Bus('my_elec_bus_1')
    >>> my_elec_bus_2 = solph.Bus('my_elec_bus_2')
    >>> my_loadink = Link(
    ...     label='link',
    ...     carrier='electricity',
    ...     from_bus=my_elec_bus_1,
    ...     to_bus=my_elec_bus_2,
    ...     capacity=100,
    ...     loss=0.04)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(
            _facade_requires_=["from_bus", "to_bus"], *args, **kwargs
        )

        self.capacity = kwargs.get("capacity")

        self.loss = kwargs.get("loss", 0)

        self.capacity_cost = kwargs.get("capacity_cost")

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.expandable = bool(kwargs.get("expandable", False))

        self.build_solph_components()

    def build_solph_components(self):
        """
        """
        investment = self._investment()

        self.inputs.update({self.from_bus: Flow(), self.to_bus: Flow()})

        self.outputs.update(
            {
                self.from_bus: Flow(
                    variable_costs=self.marginal_cost,
                    nominal_value=self._nominal_value(),
                    investment=investment,
                ),
                self.to_bus: Flow(
                    nominal_value=self._nominal_value(),
                    investment=investment
                ),
            }
        )

        self.conversion_factors.update(
            {
                (self.from_bus, self.to_bus): sequence((1 - self.loss)),
                (self.to_bus, self.from_bus): sequence((1 - self.loss)),
            }
        )


class Commodity(Source, Facade):
    """ Commodity element with one output for example a biomass commodity

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the unit is connected to with its output
    amount: numeric
        Total available amount to be used within the complete timehorzion
        of the problem
    marginal_cost: numeric
        Marginal cost for one unit used commodity
    output_paramerters: dict (optional)
        Parameters to set on the output edge of the component (see. oemof.solph
        Edge/Flow class for possible arguments)


    .. math::
        \sum_{t} x^{flow}(t) \leq c^{amount}

    For constraints set through `output_parameters` see oemof.solph.Flow class.


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_commodity = Commodity(
    ...     label='biomass-commodity',
    ...     bus=my_bus,
    ...     carrier='biomass',
    ...     amount=1000,
    ...     marginal_cost=10,
    ...     output_parameters={
    ...         'max': [0.9, 0.5, 0.4]})

    """

    def __init__(self, *args, **kwargs):
        kwargs.update({"_facade_requires_": ["bus", "carrier", "amount"]})
        super().__init__(*args, **kwargs)

        self.amount = kwargs.get("amount")

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.output_parameters = kwargs.get("output_parameters", {})

        self.build_solph_components()

    def build_solph_components(self):
        """
        """

        f = Flow(
            nominal_value=self.amount,
            variable_costs=self.marginal_cost,
            summed_max=1,
            **self.output_parameters
        )

        self.outputs.update({self.bus: f})


class Excess(Sink, Facade):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(_facade_requires_=["bus"], *args, **kwargs)

        self.bus = kwargs.get("bus")

        self.marginal_cost = kwargs.get("marginal_cost")

        self.inputs.update({self.bus: Flow(variable_costs=self.marginal_cost)})


class Shortage(Dispatchable):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Generator(Dispatchable):
    """
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


TYPEMAP = {
    "backpressure": BackpressureTurbine,
    "bus": Bus,
    "commodity": Commodity,
    "conversion": Conversion,
    "dispatchable": Dispatchable,
    "electrical bus": ElectricalBus,
    "electrical line": ElectricalLine,
    "excess": Excess,
    "extraction": ExtractionTurbine,
    "generator": Generator,
    "link": Link,
    "load": Load,
    "reservoir": Reservoir,
    "shortage": Shortage,
    "storage": Storage,
    "volatile": Volatile,
}

TECH_COLOR_MAP = {
    "acaes": "brown",
    "ocgt": "gray",
    "st": "darkgray",
    "ccgt": "lightgray",
    "pv": "gold",
    "onshore": "skyblue",
    "offshore": "darkblue",
    "ce": "olivedrab",
    "battery": "lightsalmon",
    "ror": "aqua",
    "phs": "darkblue",
    "reservoir": "slateblue",
    "biomass": "olivedrab",
    "storage": "lightsalmon",
    "battery": "lightsalmon",
    "import": "crimson",
}

CARRIER_COLER_MAP = {
    "biomass": "olivedrab",
    "lithium": "lightsalmon",
    "electricity": "darkred",
    "hydro": "aqua",
    "hydrogen": "magenta",
    "uranium": "yellow",
    "wind": "skyblue",
    "solar": "gold",
    "gas": "lightgray",
    "lignite": "chocolate",
    "coal": "darkgray",
    "waste": "yellowgreen",
    "oil": "black",
}
