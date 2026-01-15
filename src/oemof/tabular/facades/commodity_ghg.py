from typing import Optional

from oemof.network.network.nodes import Node
from oemof.solph._plumbing import sequence
from oemof.solph.flows import Flow
from pyomo.core import BuildAction, Constraint
from pyomo.core.base.block import ScalarBlock

from .commodity import Commodity


class CommodityGHG(Commodity):
    r"""
    Commodity element with one output and additionally green house gas outputs.

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

    Notes
    -----
    Emission buses carring the green house gases (GHG) are defined by starting
    with 'emission_bus', see Examples section.
    Emission factors are defined by the following naming convention:
    'emission_factor_<label_of_emission_bus>.
    The realation between the main output (`bus`) and the emission buses are
    set via :class:`~oemof.tabular.facades.commodity_ghg.CommodityGHGBlock`.

    For additional constraints set through `output_parameters` see
    oemof.solph.Flow class.

    Examples
    ---------
    Defining a ConversionGHG:

    >>> from oemof import solph

    >>> bus_gas = solph.Bus("gas")
    >>> bus_co2 = solph.Bus("co2")
    >>> bus_gas.type, bus_co2.type = "bus", "bus"

    >>> commodity = CommodityGHG(
    ...    label="gas-commodity",
    ...    bus=bus_gas,
    ...    emission_bus_0=bus_co2,
    ...    carrier="gas",
    ...    amount=1000,
    ...    marginal_cost=10,
    ...    output_parameters={"max": [0.9, 0.5, 0.4]},
    ...    emission_factor_co2=56)

    >>> commodity.emission_factors[bus_co2].default
    56
    """

    def __init__(
        self,
        label: str,
        bus: Node,
        carrier: str,
        amount: float,
        marginal_cost: float = 0,
        output_parameters: Optional[dict] = None,
        **kwargs,
    ):
        buses = {
            key: kwargs.pop(key)
            for key, value in list(
                kwargs.items()
            )  # must be turned into a list to pop from it
            if isinstance(value, Node)
        }
        super().__init__(
            label=label,
            bus=bus,
            carrier=carrier,
            amount=amount,
            marginal_cost=marginal_cost,
            output_parameters=output_parameters,
            **kwargs,
        )

        self.build_solph_components()
        self.init_emission_buses(buses)
        self.emission_factors = self.init_emission_factors(buses, kwargs)

    def init_emission_buses(self, buses):
        """Adds emissions buses as output flows and drops them from kwargs"""
        for key, value in buses.items():
            if key.startswith("emission_bus"):
                # then value is a solph.Bus object and is added to self.outputs
                self.outputs.update({value: Flow(bidirectional=True)})

    def init_emission_factors(self, buses, kwargs):
        """Returns emission factors as values in dict with buses as keys"""
        emission_factors = {}
        for key, value in kwargs.items():
            if key.startswith("emission_factor"):
                bus_label = key.removeprefix("emission_factor_")
                try:
                    bus = [
                        bus
                        for bus in buses.items()
                        if bus[1].label == bus_label
                    ][0][1]
                except IndexError:
                    raise Warning(
                        f"Emission factor is given for a non-existent emission"
                        f" bus: '{bus_label}'. Check your inputs for "
                        f"'{self.label}' of type '{self.type}'. "
                    )
                emission_factors.update({bus: sequence(value)})
        return emission_factors

    def constraint_group(self):
        return CommodityGHGBlock


class CommodityGHGBlock(ScalarBlock):
    r"""
    Block for the linear relation of nodes with type
    :class:`~oemof.tabular.facades.commodity_ghg.CommodityGHGBlock`

    **The following sets are created:**

    CommodityGHGs
        A set with all
        :class:`~oemof.tabular.facades.commodity_ghg.CommodityGHGBlock`
        objects.

    **The following constraints are created:**

    Linear relation :attr:`om.CommodityGHGBlock.relation[o,t]`
        .. math::
            P_{n.bus}(p, t) \cdot \eta_{o}(t) = P_{o}(p, t),  \\
            \forall p, t \in \textrm{TIMEINDEX}, \\
            \forall n \in \textrm{CommodityGHGs}, \\
            \forall o \in \textrm{OUTPUTS}

    While OUPUTS the set of Bus objects connected with the output of
    the CommodityGHG. The constraint above will be created for all OUTPUTS for
    all TIMESTEPS. A CommodityGHG with two outflows for one day with an hourly
    resolution will lead to 48 constraints.

    The index :math: n is the index for the Source node itself. Therefore,
    a `flow[i, n, p, t]` is a flow from the Bus i to the Source n at
    time index p, t.

    ======================  ============================  ====================
    symbol                  attribute                     explanation
    ======================  ============================  ====================
    :math:`P_{n,n.bus}(p, t)` `flow[n, n.bus, p, t]`      CommodityGHG, outflow

    :math:`P_{n,o}(p, t)`   `flow[n, o, p, t]`            CommodityGHG, outflow

    :math:`\eta_{o}(t)`     `emission_factor[n, o, t]`    Outflow, efficiency

    ======================  ============================  ====================

    """

    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        Creates the linear constraint for the class:`CommodityGHGBlock` block.
        """
        if group is None:
            return None

        m = self.parent_block()

        out_flows = {n: [o for o in n.outputs.keys()] for n in group}

        self.relation = Constraint(
            [
                (n, o, t)
                for t in m.TIMESTEPS
                for n in group
                for o in out_flows[n]
            ],
            noruleinit=True,
        )

        def _emission_relation(block):
            for t in m.TIMESTEPS:
                for n in group:
                    for o in out_flows[n]:
                        # only emission buses
                        if o is not n.bus:
                            try:
                                lhs = (
                                    m.flow[n, n.bus, t]
                                    * n.emission_factors[o][t]
                                )
                                rhs = m.flow[n, o, t]
                                block.relation.add((n, o, t), (lhs == rhs))
                            except KeyError:
                                raise KeyError(
                                    "Error in constraint creation",
                                    "source: {0}, target: {1}. You supposedly "
                                    "forgot to define an emission factor for "
                                    "this target.".format(n.label, o.label),
                                )

        self.relation_build = BuildAction(rule=_emission_relation)
