from typing import Optional

from oemof.solph._plumbing import sequence
from oemof.solph.buses import Bus
from oemof.solph.components import Link
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade


class Link(Facade, Link):
    """Bidirectional link for two buses, e.g. to model transshipment.

    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the link unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the link unit is connected to with
        its output.
    from_to_capacity: numeric
        The maximal capacity (output side to bus) of the unit. If not
        set, attr `capacity_cost` needs to be set.
    to_from_capacity: numeric
        The maximal capacity (output side from bus) of the unit. If not
        set, attr `capacity_cost` needs to be set.
    loss:
        Relative loss through the link (default: 0)
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing
        the chp capacity.
    marginal_cost: numeric
        Cost per unit Transport in each timestep. Default: 0
    expandable: boolean
        True, if capacity can be expanded within optimization. Default:
        False.


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
    ...     from_to_capacity=100,
    ...     to_from_capacity=80,
    ...     loss=0.04)
    """

    def __init__(
        self,
        label: str,
        from_bus: Bus,
        to_bus: Bus,
        carrier: Optional[str] = None,
        tech: Optional[str] = None,
        capacity: Optional[float] = None,
        from_to_capacity: Optional[float] = None,
        to_from_capacity: Optional[float] = None,
        loss: float = 0,
        capacity_cost: Optional[float] = None,
        marginal_cost: float = 0,
        expandable: bool = False,
        limit_direction: bool = False,
        **kwargs
    ):
        self.from_bus = from_bus
        self.to_bus = to_bus
        self.carrier = carrier
        self.tech = tech
        self.from_to_capacity = from_to_capacity or capacity
        self.to_from_capacity = to_from_capacity or capacity
        self.loss = loss
        self.capacity_cost = capacity_cost
        self.marginal_cost = marginal_cost
        self.expandable = expandable
        self.limit_direction = limit_direction

        super().__init__(label=label, **kwargs)

    def build_solph_components(self):
        """ """
        self.inputs.update({self.from_bus: Flow(), self.to_bus: Flow()})

        self.outputs.update(
            {
                self.from_bus: Flow(
                    variable_costs=self.marginal_cost,
                    nominal_capacity=self._nominal_capacity()["to_from"],
                ),
                self.to_bus: Flow(
                    variable_costs=self.marginal_cost,
                    nominal_capacity=self._nominal_capacity()["from_to"],
                ),
            }
        )

        self.conversion_factors.update(
            {
                (self.from_bus, self.to_bus): sequence((1 - self.loss)),
                (self.to_bus, self.from_bus): sequence((1 - self.loss)),
            }
        )
