from typing import Optional, Sequence, Union

from oemof.solph import Bus, Flow, Investment
from oemof.solph.components import GenericStorage

from oemof.tabular._facade import Facade


class Storage(Facade, GenericStorage):
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

    def __init__(
        self,
        label: str,
        bus: Bus,
        carrier: str,
        tech: str,
        storage_capacity: float = 0,
        capacity: float = 0,
        capacity_cost: float = 0,
        storage_capacity_cost: Optional[float] = None,
        storage_capacity_potential: float = float("+inf"),
        capacity_potential: float = float("+inf"),
        expandable: bool = False,
        lifetime: Optional[int] = None,
        age: int = 0,
        fixed_costs: Union[float, Sequence[float]] = 0,
        marginal_cost: float = 0,
        efficiency: float = 1,
        input_parameters: Optional[dict] = None,
        output_parameters: Optional[dict] = None,
        **kwargs
    ):
        self.bus = bus
        self.carrier = carrier
        self.tech = tech
        self.storage_capacity = storage_capacity
        self.capacity = capacity
        self.capacity_cost = capacity_cost
        self.storage_capacity_cost = storage_capacity_cost
        self.storage_capacity_potential = storage_capacity_potential
        self.capacity_potential = capacity_potential
        self.expandable = expandable
        self.lifetime = lifetime
        self.age = age
        self.fixed_costs = fixed_costs
        self.marginal_cost = marginal_cost
        self.input_parameters = input_parameters or {}
        self.output_parameters = output_parameters or {}

        self.nominal_storage_capacity = self.storage_capacity

        # make it investment but don't set costs (set below for flow (power))
        self.nominal_capacity = self._investment()

        inputs, outputs = self.__init_flows()

        super().__init__(
            label=label,
            nominal_capacity=self.nominal_capacity,
            inflow_conversion_factor=efficiency,
            outflow_conversion_factor=efficiency,
            inputs=inputs,
            outputs=outputs,
            **kwargs,
        )

    def __init_flows(self):
        if self.nominal_capacity:
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
                nominal_capacity=Investment(
                    ep_costs=self.capacity_cost,
                    maximum=self._get_maximum_additional_invest(
                        "capacity_potential", "capacity"
                    ),
                    existing=self.capacity,
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                    fixed_costs=getattr(self, "fixed_costs", None),
                ),
                **self.input_parameters,
            )
            # set investment, but no costs (as relation input / output = 1)
            fo = Flow(
                nominal_capacity=Investment(
                    existing=self.capacity,
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                ),
                variable_costs=self.marginal_cost,
                **self.output_parameters,
            )
            # required for correct grouping in oemof.solph.components
            self._invest_group = True
        else:
            fi = Flow(
                nominal_capacity=self._nominal_capacity(),
                **self.input_parameters,
            )
            fo = Flow(
                nominal_capacity=self._nominal_capacity(),
                variable_costs=self.marginal_cost,
                **self.output_parameters,
            )

        return {self.bus: fi}, {self.bus: fo}

    def build_solph_components(self) -> None:
        pass
