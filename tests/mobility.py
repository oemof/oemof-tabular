import mobility_plotting as mp
import pandas as pd
from pyomo import environ as po
from pyomo.core.base.block import ScalarBlock

from oemof import solph
from oemof.tabular.facades import Excess, Load, Shortage, Volatile
from oemof.tabular.facades.experimental.battery_electric_vehicle import Bev
from oemof.tabular.postprocessing import calculations


def double_with_offset(lst):
    result = []
    for i in range(len(lst) - 1):
        result.append((lst[i], lst[i + 1]))
    return result


def var2str(var):
    return "_".join(
        [i.label if not isinstance(i, int) else str(i) for i in var]
    )


def equate_bev_invest(model, energysystem):
    for node in energysystem.nodes:
        if isinstance(node, Bev):
            invest_vars = list(
                set(
                    inv
                    for inv in model.InvestmentFlowBlock.invest
                    for edge in inv[:2]
                    if node.facade_label in edge.label
                )
            )
            # TODO take care of multi period, only chain within period
            for var1, var2 in double_with_offset(invest_vars):
                solph.constraints.equate_variables(
                    model=model,
                    var1=model.InvestmentFlowBlock.invest[var1],
                    var2=model.InvestmentFlowBlock.invest[var2],
                    name=f"equal_invest({var2str(var1)}__{var2str(var2)})",
                )


# def relate_bev_invest(model, energysystem):
#     invest_vars = {}
#     for node in energysystem.nodes:
#         if isinstance(node, Bev):
#             invest_vars.update({
#                     node.facade_label: inv for inv in model.InvestmentFlowBlock.invest
#                     if f"{node.facade_label}-storage" in inv[1].label
#                     for edge in inv[:1]
#                     if node.electricity_bus.label in edge.label
#                     # and f"{node.facade_label}-storage" in edge.label)
#             } )
#     factors = dict.fromkeys(invest_vars.keys(), 0.3)
def relate_bev_invest(model, energysystem):
    invest_vars = []
    for node in energysystem.nodes:
        if isinstance(node, Bev):
            invest_vars.extend(
                [
                    inv
                    for inv in model.InvestmentFlowBlock.invest
                    if f"{node.facade_label}-storage" in inv[1].label
                    for edge in inv[:1]
                    if node.electricity_bus.label in edge.label
                    # and f"{node.facade_label}-storage" in edge.label)
                ]
            )
    market_share = dict(zip(invest_vars, [0.3, 0.1, 0.6]))

    model.TotalBevInvest = po.Var(model.PERIODS, within=po.NonNegativeReals)
    # m.PERIODS,

    def total_bev_invest_rule(m):
        return m.TotalBevInvest[p] == sum(
            m.InvestmentFlowBlock.invest[inv_var] for inv_var in invest_vars
        )

    for p in model.PERIODS:
        name = f"total_bev_invest-({p})"
        setattr(model, name, po.Constraint(rule=total_bev_invest_rule))

    # model.total_investment_constraint = po.Constraint(
    #     expr=sum(model.InvestmentFlowBlock.invest[inv_var] for inv_var in
    #              invest_vars) == model.TotalBevInvest[period]
    # )

    # model.investment_constraints = po.ConstraintList()
    # for inv_var in invest_vars:
    #     model.investment_constraints.add(
    #         model.InvestmentFlowBlock.invest[inv_var] == factors[
    #             inv_var] * model.total_bev_invest
    #
    #     )

    # Define the rule to set the investment constraints
    def investment_constraints_rule(m):
        return (
            m.InvestmentFlowBlock.invest[inv_var]
            == market_share[inv_var] * m.TotalBevInvest[p]
        )

    for p in model.PERIODS:
        for inv_var in invest_vars:
            name = f"bev_invest_share({var2str(inv_var)})"
            setattr(
                model, name, po.Constraint(rule=investment_constraints_rule)
            )

    # model.BevBlock = OrderedScalarSet(
    #     ordered_constraints=[model.TotalBevInvest, model.constraint2,
    #                          model.constraint3])

    # setattr(model, name, po.Constraint(rule=relate_variables_rule))
    # # for var1, var2 in double_with_offset(invest_vars):
    # relate_variables(
    #     model=model,
    #     var1=model.InvestmentFlowBlock.invest[invest_vars[0]],
    #     var2=model.InvestmentFlowBlock.invest[invest_vars[1]],
    #     var3=model.InvestmentFlowBlock.invest[invest_vars[2]],
    #     factor1=0.2,
    #     factor2=0.3,
    #     factor3=0.5,
    #     name="test"
    #     # name=f"fixed_bev_share({var2str(var1)}__{var2str(var2)})",
    #     )


# def relate_variables(model, vars, factors, name=None
#                      ):
#
#     if name is None:
#         name = "_".join(["relate", str(var1), str(var2), str(var3)])
#
#     def relate_variables_rule(m):
#         return var1 * factor1 + var2 * factor2 + var3 * factor3 == v
#
#     setattr(model, name, po.Constraint(rule=relate_variables_rule))


def relate_variables(
    model, var1, var2, var3, factor1, factor2, factor3, name=None
):
    if name is None:
        name = "_".join(["relate", str(var1), str(var2), str(var3)])

    def relate_variables_rule(m):
        return (
            var1 * factor1 + var2 * factor2 + var3 * factor3
            == factor1 + factor2 + factor3
        )

    setattr(model, name, po.Constraint(rule=relate_variables_rule))


class BevInvestmentBlock(ScalarBlock):
    CONSTRAINT_GROUP = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        if group is None:
            return None

        m = self.parent_block()

        # Set of DSM Components
        self.bev = po.Set(initialize=[n for n in group])

        self.TotalBevInvest = po.Var(m.PERIODS, within=po.NonNegativeReals)

        def relate_bev_invest(self):
            invest_vars = []
            for node in self.es.nodes:
                if isinstance(node, Bev):
                    invest_vars.extend(
                        [
                            inv
                            for inv in model.InvestmentFlowBlock.invest
                            if f"{node.facade_label}-storage" in inv[1].label
                            for edge in inv[:1]
                            if node.electricity_bus.label in edge.label
                            # and f"{node.facade_label}-storage" in edge.label)
                        ]
                    )
            market_share = dict(zip(invest_vars, [0.3, 0.1, 0.6]))
            return invest_vars, market_share

            # m.PERIODS,

        def total_bev_invest_rule(m):
            return m.TotalBevInvest[p] == sum(
                m.InvestmentFlowBlock.invest[inv_var]
                for inv_var in invest_vars
            )

        invest_vars, market_share = relate_bev_invest()
        for p in model.PERIODS:
            name = f"total_bev_invest-({p})"
            setattr(
                model, name, po.Constraint(group, rule=total_bev_invest_rule)
            )


if __name__ == "__main__":
    date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")

    energysystem = solph.EnergySystem(
        groupings=solph.GROUPINGS,
        timeindex=date_time_index,
        infer_last_interval=True,
    )

    el_bus = solph.Bus("el-bus")
    el_bus.type = "bus"
    energysystem.add(el_bus)

    indiv_mob = solph.Bus("pkm-bus")
    indiv_mob.type = "bus"
    energysystem.add(indiv_mob)

    volatile = Volatile(
        type="volatile",
        label="wind",
        bus=el_bus,
        carrier="wind",
        tech="onshore",
        capacity=200,
        capacity_cost=1,
        expandable=True,
        # expandable=False,
        # capacity_potential=1e8,
        profile=[1, 0, 1],
    )
    energysystem.add(volatile)

    load = Load(
        label="load",
        type="load",
        carrier="electricity",
        bus=el_bus,
        amount=100,
        profile=[1, 1, 1],
    )
    energysystem.add(load)

    excess = Excess(
        type="excess",
        label="excess",
        bus=el_bus,
        carrier="electricity",
        tech="excess",
        capacity=100,
        marginal_cost=10,
    )
    energysystem.add(excess)

    shortage = Shortage(
        type="shortage",
        label="shortage",
        bus=el_bus,
        carrier="electricity",
        tech="shortage",
        capacity=100,
        marginal_cost=1e6,
    )
    energysystem.add(shortage)

    pkm_demand = Load(
        label="pkm_demand",
        type="Load",
        carrier="pkm",
        bus=indiv_mob,
        amount=200,  # PKM
        profile=[0, 1, 0],  # drive consumption
    )

    energysystem.add(pkm_demand)

    bev_v2g = Bev(
        type="bev",
        label="BEV-V2G",
        electricity_bus=el_bus,
        storage_capacity=150,
        capacity=50,
        drive_power=150,  # nominal value sink
        # drive_consumption=[1, 1, 1],  # relative value sink
        max_charging_power=0,  # existing
        availability=[1, 1, 1],
        efficiency_charging=1,
        v2g=True,
        # loss_rate=0.01,
        # min_storage_level=[0.1, 0.2, 0.15, 0.15],
        # max_storage_level=[0.9, 0.95, 0.92, 0.92],
        transport_commodity_bus=indiv_mob,
        expandable=True,
        bev_capacity_cost=2,
        invest_c_rate=0.5,
        # marginal_cost=3,
        pkm_conversion_rate=0.7,
    )
    energysystem.add(bev_v2g)

    bev_flex = Bev(
        type="bev",
        label="BEV-FLEX",
        electricity_bus=el_bus,
        storage_capacity=200,
        drive_power=100,
        # drive_consumption=[0, 1, 0],
        # max_charging_power=200,
        availability=[1, 1, 1],
        v2g=False,
        # loss_rate=0.01,
        # min_storage_level=[0.1, 0.2, 0.15, 0.15],
        # max_storage_level=[0.9, 0.95, 0.92, 0.92],
        transport_commodity_bus=indiv_mob,
        expandable=True,
        bev_capacity_cost=2,
        invest_c_rate=1,
        # marginal_cost=3,
        pkm_conversion_rate=0.7,
    )
    energysystem.add(bev_flex)

    bev_fix = Bev(
        type="bev",
        label="BEV-FIX",
        electricity_bus=el_bus,
        storage_capacity=200,
        drive_power=100,
        # drive_consumption=[0, 1, 0],
        # max_charging_power=200,
        availability=[1, 1, 1],
        v2g=False,
        # loss_rate=0.01,
        # min_storage_level=[0.1, 0.2, 0.15, 0.15],
        # max_storage_level=[0.9, 0.95, 0.92, 0.92],
        transport_commodity_bus=indiv_mob,
        expandable=True,
        bev_capacity_cost=2,
        invest_c_rate=60 / 20,  # Capacity/Power
        # marginal_cost=3,
        pkm_conversion_rate=0.7,
        input_parameters={"fix": [0, 0, 0]},  # fixed relative charging profile
    )
    energysystem.add(bev_fix)

    mp.draw_graph(energysystem)

    model = solph.Model(
        energysystem,
        timeindex=energysystem.timeindex,
    )

    filepath = "./mobility.lp"
    model.write(filepath, io_options={"symbolic_solver_labels": True})

    # extra constraints
    equate_bev_invest(model, energysystem)
    #
    # relate_bev_invest(model, energysystem)
    BevInvestmentBlock._create(group="bev")

    filepath = "./mobility_constrained.lp"
    model.write(filepath, io_options={"symbolic_solver_labels": True})

    # select solver 'gurobi', 'cplex', 'glpk' etc
    model.solve("cbc", solve_kwargs={"tee": True})

    energysystem.params = solph.processing.parameter_as_dict(
        energysystem, exclude_attrs=["subnodes"]
    )
    energysystem.results = model.results()

    # Rename results for easy access
    energysystem.new_results = {}
    for r in energysystem.results:
        if r[1] is not None:
            energysystem.new_results[
                f"{r[0].label}: {r[1].label}"
            ] = energysystem.results[r]

    # postprocessing
    postprocessed_results = calculations.run_postprocessing(energysystem)

    # # plot bev results
    # mp.plot_bev_results(
    #     energysystem=energysystem,
    #     facade_label=["BEV-V2G", "BEV-FLEX"]
    # )

    print(postprocessed_results)
