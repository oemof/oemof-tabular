from dataclasses import field

from oemof.solph import Bus, Flow, Investment
from oemof.solph._plumbing import sequence
from oemof.solph.components import GenericStorage

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Storage(GenericStorage, Facade):
    r"""Storage unit

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total capacity of the storage (e.g. in MWh)
    capacity: numeric
        Maximum production capacity (e.g. in MW)
    efficiency: numeric
        Efficiency of charging and discharging process: Default: 1
    storage_capacity_cost: numeric
        Investment costs for the storage unit e.g in €/MWh-capacity
    capacity_cost: numeric
        Investment costs for the storage unit e.g in €/MW-capacity
    expandable: boolean
        True, if capacity can be expanded within optimization. Default: False.
    lifetime: int (optional)
        Lifetime of the component in years. Necessary for multi-period
        investment optimization. Default: None.
    storage_capacity_potential: numeric
        Potential of the investment for storage capacity in MWh. Default: +inf.
    capacity_potential: numeric
        Potential of the investment for capacity in MW. Default: +inf.
    input_parameters: dict (optional)
        Set parameters on the input edge of the storage (see oemof.solph for
        more information on possible parameters)
    output_parameters: dict (optional)
        Set parameters on the output edge of the storage (see oemof.solph for
        more information on possible parameters)


    Intertemporal energy balance of the storage:

    .. math::

        x^{level}(t) =
        x^{level}(t-1) \cdot (1 - c^{loss\_rate})
        + \sqrt{c^{efficiency}(t)}  x^{flow, in}(t)
        - \frac{x^{flow, out}(t)}{\sqrt{c^{efficiency}(t)}}\\
        \qquad \forall t \in T

    .. math::
        x^{level}(0) = 0.5 \cdot c^{capacity}

    The **expression** added to the cost minimizing objective funtion
    for the operation is given as:

    .. math::

        x^{opex} = \sum_t (x^{flow, out}(t) \cdot c^{marginal\_cost}(t))


    Examples
    ---------

    >>> import pandas as pd
    >>> from oemof import solph
    >>> from oemof.tabular import facades as fc
    >>> my_bus = solph.Bus('my_bus')
    >>> es = solph.EnergySystem(
    ...    timeindex=pd.date_range('2019', periods=3, freq='H'))
    >>> es.add(my_bus)
    >>> es.add(
    ...    fc.Storage(
    ...        label="storage",
    ...        bus=my_bus,
    ...        carrier="lithium",
    ...        tech="battery",
    ...        storage_capacity_cost=10,
    ...        invest_relation_output_capacity=1/6, # oemof.solph
    ...        marginal_cost=5,
    ...        balanced=True, # oemof.solph argument
    ...        initial_storage_level=1, # oemof.solph argument
    ...        max_storage_level=[0.9, 0.95, 0.8])) # oemof.solph argument

    """
    bus: Bus

    carrier: str

    tech: str

    storage_capacity: float = 0

    capacity: float = 0

    capacity_cost: float = 0

    storage_capacity_cost: float = None

    storage_capacity_potential: float = float("+inf")

    capacity_potential: float = float("+inf")

    expandable: bool = False

    lifetime: int = None

    marginal_cost: float = 0

    efficiency: float = 1

    input_parameters: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        """ """
        self.nominal_storage_capacity = self.storage_capacity

        self.inflow_conversion_factor = sequence(self.efficiency)

        self.outflow_conversion_factor = sequence(self.efficiency)

        # make it investment but don't set costs (set below for flow (power))
        self.investment = self._investment()

        if self.investment:
            self.invest_relation_input_output = 1

            for attr in ["invest_relation_input_output"]:
                if getattr(self, attr) is None:
                    raise AttributeError(
                        (
                            "You need to set attr " "`{}` " "for component {}"
                        ).format(attr, self.label)
                    )

            # set capacity costs at one of the flows
            fi = Flow(
                investment=Investment(
                    ep_costs=self.capacity_cost,
                    maximum=self._get_maximum_additional_invest(
                        "capacity_potential", "capacity"
                    ),
                    existing=self.capacity,
                    lifetime=getattr(self, "lifetime", None),
                ),
                **self.input_parameters,
            )
            # set investment, but no costs (as relation input / output = 1)
            fo = Flow(
                investment=Investment(existing=self.capacity,
                                      lifetime=getattr(self, "lifetime", None),
                                      ),
                variable_costs=self.marginal_cost,
                **self.output_parameters,
            )
            # required for correct grouping in oemof.solph.components
            self._invest_group = True
        else:
            fi = Flow(
                nominal_value=self._nominal_value(), **self.input_parameters
            )
            fo = Flow(
                nominal_value=self._nominal_value(),
                variable_costs=self.marginal_cost,
                **self.output_parameters,
            )

        self.inputs.update({self.bus: fi})

        self.outputs.update({self.bus: fo})

        self._set_flows()
