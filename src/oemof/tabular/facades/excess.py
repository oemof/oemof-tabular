from dataclasses import field

from oemof.solph.buses import Bus
from oemof.solph.components import Sink
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Excess(Sink, Facade):
    """ """

    bus: Bus

    marginal_cost: float = 0

    capacity: float = None

    capacity_potential: float = float("+inf")

    capacity_cost: float = None

    capacity_minimum: float = None

    expandable: bool = False

    input_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
        f = Flow(
            nominal_value=self._nominal_value(),
            variable_costs=self.marginal_cost,
            investment=self._investment(),
            **self.input_parameters,
        )

        self.inputs.update({self.bus: f})
