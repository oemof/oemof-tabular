from dataclasses import field
from typing import Sequence, Union

from oemof.solph.buses import Bus
from oemof.solph.components import Sink
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Load(Sink, Facade):
    r"""Load object with one input

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the demand is connected to.
    amount: numeric
        The total amount for the timehorzion (e.g. in MWh)
    profile: array-like
        Load profile with normed values such that `profile[t] * amount`
        yields the load in timestep t (e.g. in MWh)
    marginal_utility: numeric
        Marginal utility in for example Euro / MWh
    input_parameters: dict (optional)



    .. math::
        x^{flow}(t) = c^{amount}(t)  \cdot x^{flow}(t) \qquad \forall t \in T


    Examples
    ---------

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_load = Load(
    ...     label='load',
    ...     carrier='electricity',
    ...     bus=my_bus,
    ...     amount=100,
    ...     profile=[0.3, 0.2, 0.5])
    """

    bus: Bus

    amount: float

    profile: Union[float, Sequence[float]]

    marginal_utility: float = 0

    input_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
        self.inputs.update(
            {
                self.bus: Flow(
                    nominal_value=self.amount,
                    fix=self.profile,
                    variable_costs=self.marginal_utility,
                    **self.input_parameters,
                )
            }
        )
