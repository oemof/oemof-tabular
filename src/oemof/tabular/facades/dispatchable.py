from dataclasses import field
from typing import Sequence, Union

from oemof.solph.components import Source
from oemof.solph.flows import Flow
from oemof.solph.buses import Bus

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Dispatchable(Source, Facade):
    r""" Dispatchable element with one output for example a gas-turbine

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
    capacity_minimum: numeric
        Minimum install capacity if capacity is to be expanded


    The mathematical representations for these components are dependent on the
    user defined attributes. If the capacity is fixed before
    (**dispatch mode**) the following equation holds:

    .. math::

        x^{flow}(t) \leq c^{capacity} \cdot c^{profile}(t) \
        \qquad \forall t \in T

    Where :math:`x^{flow}` denotes the production (endogenous variable)
    of the dispatchable object to the bus.

    If `expandable` is set to `True` (**investment mode**), the equation
    changes slightly:

    .. math::

        x^{flow}(t) \leq (x^{capacity} +
        c^{capacity})  \cdot c^{profile}(t) \qquad \forall t \in T

    Where the bounded endogenous variable of the volatile component is added:

    ..  math::

            x^{capacity} \leq c^{capacity\_potential}

    **Objective expression** for operation:

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
    ...         'min': 0.2})

    """
    bus: Bus

    carrier: str

    tech: str

    profile: Union[float, Sequence[float]] = 1

    capacity: float = None

    capacity_potential: float = float("+inf")

    marginal_cost: float = 0

    capacity_cost: float = None

    capacity_minimum: float = None

    expandable: bool = False

    output_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """

        if self.profile is None:
            self.profile = 1

        f = Flow(
            nominal_value=self._nominal_value(),
            variable_costs=self.marginal_cost,
            max=self.profile,
            investment=self._investment(),
            **self.output_parameters,
        )

        self.outputs.update({self.bus: f})
