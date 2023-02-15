from dataclasses import field

from oemof.solph import Bus, Flow, Transformer
from oemof.solph.plumbing import sequence

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Conversion(Transformer, Facade):
    r"""Conversion unit with one input and one output.

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
    capacity_minimum: numeric
        Minimum invest capacity in unit of output capacity.
    input_parameters: dict (optional)
        Set parameters on the input edge of the conversion unit
        (see oemof.solph for more information on possible parameters)
    ouput_parameters: dict (optional)
        Set parameters on the output edge of the conversion unit
         (see oemof.solph for more information on possible parameters)


    .. math::
        x^{flow, from}(t) \cdot c^{efficiency}(t) = x^{flow, to}(t)
        \qquad \forall t \in T

    **Objective expression** for operation includes marginal cost and/or
    carrier costs:

        .. math::

            x^{opex} =  \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t)
            + x^{flow, carrier}(t) \cdot c^{carrier\_cost}(t))


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
    from_bus: Bus

    to_bus: Bus

    carrier: str

    tech: str

    capacity: float = None

    efficiency: float = 1

    marginal_cost: float = 0

    carrier_cost: float = 0

    capacity_cost: float = None

    expandable: bool = False

    capacity_potential: float = float("+inf")

    capacity_minimum: float = None

    input_parameters: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
        self.conversion_factors.update(
            {
                self.from_bus: sequence(1),
                self.to_bus: sequence(self.efficiency),
            }
        )

        self.inputs.update(
            {
                self.from_bus: Flow(
                    variable_costs=self.carrier_cost, **self.input_parameters
                )
            }
        )

        self.outputs.update(
            {
                self.to_bus: Flow(
                    nominal_value=self._nominal_value(),
                    variable_costs=self.marginal_cost,
                    investment=self._investment(),
                    **self.output_parameters,
                )
            }
        )
