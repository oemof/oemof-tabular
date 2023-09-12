from dataclasses import field
from typing import Sequence, Union

from oemof.solph.buses import Bus
from oemof.solph.components import Source
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Volatile(Source, Facade):
    r"""Volatile element with one output. This class can be used to model
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
    capacity_minimum: numeric
        Minimum install capacity if investment
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


    The mathematical representations for this components are dependent on the
    user defined attributes. If the capacity is fixed before
    (**dispatch mode**) the following equation holds:

    .. math::

        x^{flow}(t) = c^{capacity} \cdot c^{profile}(t) \qquad \forall t \in T

    Where :math:`x_{volatile}^{flow}` denotes the production
    (endogenous variable) of the volatile object to the bus.

    If `expandable` is set to `True` (**investment mode**), the equation
    changes slightly:

    .. math::

        x^{flow}(t) = (x^{capacity} + c^{capacity}) \
         \cdot c^{profile}(t)  \qquad \forall t \in T

    Where the bounded endogenous variable of the volatile component is added:

    ..  math::

            x_{volatile}^{capacity} \leq c_{volatile}^{capacity\_potential}

    **Objective expression** for operation:

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
    bus: Bus

    carrier: str

    tech: str

    profile: Union[float, Sequence[float]]

    capacity: float = None

    capacity_potential: float = float("+inf")

    capacity_minimum: float = None

    expandable: bool = False

    marginal_cost: float = 0

    capacity_cost: float = None

    lifetime: int = None

    age: int = 0

    fixed_costs: Union[float, Sequence[float]] = None

    output_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
        f = Flow(
            nominal_value=self._nominal_value(),
            variable_costs=self.marginal_cost,
            fix=self.profile,
            investment=self._investment(),
            **self.output_parameters,
        )

        self.outputs.update({self.bus: f})
