from typing import Optional

from oemof.solph.buses import Bus
from oemof.solph.components import Sink
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade


class Excess(Facade, Sink):
    """ """

    def __init__(
        self,
        label: str,
        bus: Bus,
        carrier: Optional[str] = None,
        tech: Optional[str] = None,
        marginal_cost: float = 0,
        capacity: Optional[float] = None,
        capacity_potential: float = float("+inf"),
        capacity_cost: Optional[float] = None,
        capacity_minimum: Optional[float] = None,
        expandable: bool = False,
        input_parameters: Optional[dict] = None,
        **kwargs
    ):
        self.bus = bus
        self.carrier = carrier
        self.tech = tech
        self.marginal_cost = marginal_cost
        self.capacity = capacity
        self.capacity_potential = capacity_potential
        self.capacity_cost = capacity_cost
        self.capacity_minimum = capacity_minimum
        self.expandable = expandable
        self.input_parameters = input_parameters or {}

        super().__init__(label=label, inputs={}, **kwargs)

    def build_solph_components(self):
        """ """
        f = Flow(
            nominal_capacity=self._nominal_capacity(),
            variable_costs=self.marginal_cost,
            **self.input_parameters,
        )

        self.inputs.update({self.bus: f})
