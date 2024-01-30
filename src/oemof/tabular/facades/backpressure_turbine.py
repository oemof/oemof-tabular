from dataclasses import field
from typing import Sequence, Union

from oemof.solph._plumbing import sequence
from oemof.solph.buses import Bus
from oemof.solph.components import Converter
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class BackpressureTurbine(Converter, Facade):
    r""" Combined Heat and Power (backpressure) unit with one input and
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
    lifetime: int (optional)
        Lifetime of the component in years. Necessary for multi-period
        investment optimization.
        Note: Only applicable for a multi-period model. Default: None.
    age : int (optional)
        The initial age of a flow (usually given in years);
        once it reaches its lifetime (considering also
        an initial age), the flow is forced to 0.
        Note: Only applicable for a multi-period model. Default: 0.
    fixed_costs : numeric (iterable or scalar) (optional)
        The fixed costs associated with a flow.
        Note: Only applicable for a multi-period model. Default: None.
    capacity_cost: numeric
        Investment costs per unit of electrical capacity (e.g. Euro / MW) .
        If capacity is not set, this value will be used for optimizing the
        chp capacity.


    Backpressure turbine power plants are modelled with a constant relation
    between heat and electrical output (power to heat coefficient).

    .. math::

        x^{flow, carrier}(t) =
        \frac{x^{flow, electricity}(t) + x^{flow, heat}(t)}\
        {c^{thermal\:efficiency}(t) + c^{electrical\:efficiency}(t)} \\
        \qquad \forall t \in T

    .. math::

        \frac{x^{flow, electricity}(t)}{x_{flow, thermal}(t)} =
        \frac{c^{electrical\:efficiency}(t)}{c^{thermal\:efficiency}(t)}
        \qquad \forall t \in T

    **Objective expression** for operation includes marginal cost and/or
    carrier costs:

        .. math::

            x^{opex} = \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t)
            + x^{flow, carrier}(t) \cdot c^{carrier\_cost}(t))

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

    fuel_bus: Bus

    heat_bus: Bus

    electricity_bus: Bus

    carrier: str

    tech: str

    electric_efficiency: Union[float, Sequence[float]]

    thermal_efficiency: Union[float, Sequence[float]]

    capacity: float = None

    capacity_cost: float = None

    carrier_cost: float = 0

    marginal_cost: float = 0

    expandable: bool = False

    lifetime: int = None

    age: int = 0

    fixed_costs: Union[float, Sequence[float]] = None

    input_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
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
                    investment=self._investment(),
                ),
                self.heat_bus: Flow(),
            }
        )
