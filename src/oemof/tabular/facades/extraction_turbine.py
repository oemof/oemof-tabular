from dataclasses import field
from typing import Sequence, Union

from oemof.solph import Bus, Flow
from oemof.solph.components import ExtractionTurbineCHP
from oemof.solph.plumbing import sequence

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class ExtractionTurbine(ExtractionTurbineCHP, Facade):
    r""" Combined Heat and Power (extraction) unit with one input and
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
    `ExtractionTurbineCHP <https://oemof.readthedocs.io/en/
    stable/oemof_solph.html#extractionturbinechp-component>`_ :

    .. math::
        x^{flow, carrier}(t) =
        \frac{x^{flow, electricity}(t) + x^{flow, heat}(t) \
        \cdot c^{beta}(t)}{c^{condensing\_efficiency}(t)}
        \qquad \forall t \in T

    .. math::
        x^{flow, electricity}(t)  \geq  x^{flow, thermal}(t) \cdot
        \frac{c^{electrical\_efficiency}(t)}{c^{thermal\_efficiency}(t)}
        \qquad \forall t \in T

    where :math:`c^{beta}` is defined as:

     .. math::
        c^{beta}(t) = \frac{c^{condensing\_efficiency}(t) -
        c^{electrical\_efficiency(t)}}{c^{thermal\_efficiency}(t)}
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
    carrier: str

    tech: str

    electricity_bus: Bus

    heat_bus: Bus

    fuel_bus: Bus

    condensing_efficiency: Union[float, Sequence[float]]

    electric_efficiency: Union[float, Sequence[float]]

    thermal_efficiency: Union[float, Sequence[float]]

    capacity: float = None

    carrier_cost: float = 0

    marginal_cost: float = 0

    capacity_cost: float = None

    expandable: bool = False

    input_parameters: dict = field(default_factory=dict)

    conversion_factor_full_condensation: dict = field(default_factory=dict)

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
                    variable_costs=self.marginal_cost,
                    investment=self._investment(),
                ),
                self.heat_bus: Flow(),
            }
        )

        self.conversion_factor_full_condensation.update(
            {self.electricity_bus: sequence(self.condensing_efficiency)}
        )
