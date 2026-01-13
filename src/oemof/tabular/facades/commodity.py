from typing import Optional

from oemof.solph.buses import Bus
from oemof.solph.components import Source
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade


class Commodity(Facade, Source):
    r"""Commodity element with one output for example a biomass commodity

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the unit is connected to with its output
    amount: numeric
        Total available amount to be used within the complete time horizon
        of the problem
    marginal_cost: numeric
        Marginal cost for one unit used commodity
    output_parameters: dict (optional)
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

    def __init__(
        self,
        label: str,
        bus: Bus,
        carrier: str,
        amount: float,
        marginal_cost: float = 0,
        output_parameters: Optional[dict] = None,
        **kwargs
    ):
        self.bus = bus
        self.carrier = carrier
        self.amount = amount
        self.marginal_cost = marginal_cost
        self.output_parameters = output_parameters or {}

        super().__init__(label=label, outputs={}, **kwargs)

    def build_solph_components(self):
        """ """

        f = Flow(
            nominal_capacity=self.amount,
            variable_costs=self.marginal_cost,
            full_load_time_max=1,
            **self.output_parameters,
        )

        self.outputs.update({self.bus: f})
