
from oemof.solph.components.experimental import Link

from oemof.solph.flows import Flow
from oemof.solph.buses import Bus
from oemof.solph._plumbing import sequence

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Link(Link, Facade):
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

    from_bus: Bus

    to_bus: Bus

    from_to_capacity: float = None

    to_from_capacity: float = None

    loss: float = 0

    capacity_cost: float = None

    marginal_cost: float = 0

    expandable: bool = False

    limit_direction: bool = False

    def build_solph_components(self):
        """ """
        investment = self._investment()

        self.inputs.update({self.from_bus: Flow(), self.to_bus: Flow()})

        self.outputs.update(
            {
                self.from_bus: Flow(
                    variable_costs=self.marginal_cost,
                    nominal_value=self._nominal_value()["to_from"],
                    investment=investment,
                ),
                self.to_bus: Flow(
                    variable_costs=self.marginal_cost,
                    nominal_value=self._nominal_value()["from_to"],
                    investment=investment,
                ),
            }
        )

        self.conversion_factors.update(
            {
                (self.from_bus, self.to_bus): sequence((1 - self.loss)),
                (self.to_bus, self.from_bus): sequence((1 - self.loss)),
            }
        )
