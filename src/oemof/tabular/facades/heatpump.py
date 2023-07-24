from dataclasses import field
from typing import Sequence, Union

from oemof.solph._plumbing import sequence
from oemof.solph.buses import Bus
from oemof.solph.components import Transformer
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class HeatPump(Transformer, Facade):
    r"""HeatPump unit with two inputs and one output.

    Parameters
    ----------
    low_temperature_bus: oemof.solph.Bus
        An oemof bus instance where unit is connected to with
        its low temperature input.
    high_temperature_bus: oemof.solph.Bus
        An oemof bus instance where the unit is connected to with
        its high temperature input.
    capacity: numeric
        The thermal capacity (high temperature output side) of the unit.
    cop: numeric
        Coefficienct of performance
    carrier_cost: numeric
        Carrier cost for one unit of used input. Default: 0
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        conversion output capacity.
    expandable: boolean or numeric (binary)
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
    capacity_potential: numeric
        Maximum invest capacity in unit of output capacity. Default: +inf.
    low_temperature_parameters: dict (optional)
        Set parameters on the input edge of the heat pump unit
        (see oemof.solph for more information on possible parameters)
    high_temperature_parameters: dict (optional)
        Set parameters on the output edge of the heat pump unit
        (see oemof.solph for more information on possible parameters)
    input_parameters: dict (optional)
        Set parameters on the input edge of the conversion unit
         (see oemof.solph for more information on possible parameters)


    .. math::
        x_{electricity\_bus, hp}^{flow} = \frac{1}{c^{COP}} \cdot
        x_{hp, high\_temperature\_bus}^{flow}

    .. math::
        x_{low\_temperature\_source, low\_temperature\_bus}^{flow} =
        x_{hp, high\_temperature\_bus}^{flow} \frac{c^{COP} -1}{c^{COP}}

    **Objective expression** for operation includes marginal cost and/or
    carrier costs:

        .. math::

            x^{opex} =  \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t)
            + x^{flow, carrier}(t) \cdot c^{carrier\_cost}(t))


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> electricity_bus = solph.Bus("elec-bus")
    >>> heat_bus= solph.Bus('heat_bus')
    >>> heat_bus_low = solph.Bus('heat_bus_low')
    >>> fc.HeatPump(
    ...     label="hp-storage",
    ...     carrier="electricity",
    ...     tech="hp",
    ...     cop=3,
    ...     carrier_cost=15,
    ...     electricity_bus=elec_bus,
    ...     high_temperature_bus=heat_bus,
    ...     low_temperature_bus=heat_bus_low)

    """
    electricity_bus: Bus

    high_temperature_bus: Bus

    low_temperature_bus: Bus

    carrier: str

    tech: str

    cop: float

    capacity: float = None

    marginal_cost: float = 0

    carrier_cost: float = 0

    capacity_cost: float = None

    expandable: bool = False

    lifetime: int = None

    age: int = 0

    fixed_costs: Union[float, Sequence[float]] = None

    capacity_potential: float = float("+inf")

    low_temperature_parameters: dict = field(default_factory=dict)

    high_temperature_parameters: dict = field(default_factory=dict)

    input_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
        self.conversion_factors.update(
            {
                self.electricity_bus: sequence(1 / self.cop),
                self.low_temperature_bus: sequence((self.cop - 1) / self.cop),
                self.high_temperature_bus: sequence(1),
            }
        )

        self.inputs.update(
            {
                self.electricity_bus: Flow(
                    variable_costs=self.carrier_cost, **self.input_parameters
                ),
                self.low_temperature_bus: Flow(
                    **self.low_temperature_parameters
                ),
            }
        )

        self.outputs.update(
            {
                self.high_temperature_bus: Flow(
                    nominal_value=self._nominal_value(),
                    variable_costs=self.marginal_cost,
                    investment=self._investment(),
                    **self.high_temperature_parameters,
                )
            }
        )
