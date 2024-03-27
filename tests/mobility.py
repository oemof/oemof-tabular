import os

import mobility_plotting as mp
import pandas as pd

from oemof import solph
from oemof.tabular import __path__ as tabular_path
from oemof.tabular.constraint_facades import CONSTRAINT_TYPE_MAP
from oemof.tabular.datapackage.reading import deserialize_constraints
from oemof.tabular.facades import Excess, Load, Shortage, Volatile
from oemof.tabular.facades.experimental.battery_electric_vehicle import (
    BevFleet,
    BevTech,
)
from oemof.tabular.postprocessing import calculations

if __name__ == "__main__":
    # Single-period example
    # date_time_index = pd.date_range("1/1/2020", periods=3, freq="H")
    # energysystem = solph.EnergySystem(
    #     timeindex=date_time_index,
    #     infer_last_interval=True,
    # )
    # periods=[2020]

    # Multi-period example
    t_idx_1 = pd.date_range("1/1/2020", periods=3, freq="h")
    t_idx_2 = pd.date_range("1/1/2030", periods=3, freq="h")
    t_idx_1_series = pd.Series(index=t_idx_1, dtype="float64")
    t_idx_2_series = pd.Series(index=t_idx_2, dtype="float64")
    date_time_index = pd.concat([t_idx_1_series, t_idx_2_series]).index
    periods = [t_idx_1, t_idx_2]

    energysystem = solph.EnergySystem(
        timeindex=date_time_index,
        infer_last_interval=False,
        timeincrement=[1] * len(date_time_index),
        periods=periods,
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
        profile=len(periods) * [1, 0, 1],
        lifetime=20,
    )
    energysystem.add(volatile)

    load = Load(
        label="load",
        type="load",
        carrier="electricity",
        bus=el_bus,
        amount=100,
        profile=len(periods) * [1, 1, 1],
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
        capacity=1000,
        marginal_cost=1e6,
    )
    energysystem.add(shortage)

    pkm_demand = Load(
        label="pkm_demand",
        type="Load",
        carrier="pkm",
        bus=indiv_mob,
        amount=200,  # PKM
        profile=len(periods) * [0, 1, 0],  # drive consumption
    )

    energysystem.add(pkm_demand)

    # bev_v2g = BevTech(
    #     type="bev",
    #     label="BEV-V2G",
    #     electricity_bus=el_bus,
    #     commodity_bus=indiv_mob,
    #     storage_capacity=150,
    #     # drive_power=150,  # nominal value sink
    #     # drive_consumption=[1, 1, 1],  # relative value sink
    #     charging_power=150,  # existing
    #     availability=len(periods) * [1, 1, 1],
    #     efficiency_charging=1,
    #     v2g=True,
    #     loss_rate=0.01,
    #     min_storage_level=(len(date_time_index) + 0) * [0],
    #     max_storage_level=(len(date_time_index) + 0) * [0.9],
    #     expandable=True,
    #     bev_invest_costs=2,
    #     invest_c_rate=60 / 20,  # Capacity/Power
    #     variable_costs=3,
    #     fixed_investment_costs=1,
    #     commodity_conversion_rate=0.7,
    #     lifetime=10,
    # )
    # energysystem.add(bev_v2g)
    #
    # bev_flex = BevTech(
    #     type="bev",
    #     label="BEV-inflex",
    #     electricity_bus=el_bus,
    #     commodity_bus=indiv_mob,
    #     storage_capacity=200,
    #     drive_power=100,
    #     # drive_consumption=[0, 1, 0],
    #     charging_power=200,
    #     availability=len(periods) * [1, 1, 1],
    #     v2g=False,
    #     # loss_rate=0.01,
    #     # min_storage_level=[0.1, 0.2, 0.15, 0.15],
    #     # max_storage_level=[0.9, 0.95, 0.92, 0.92],
    #     expandable=True,
    #     bev_invest_costs=2,
    #     invest_c_rate=60 / 20,
    #     variable_costs=3,
    #     fixed_investment_costs=1,
    #     commodity_conversion_rate=0.7,
    #     lifetime=10,
    # )
    # energysystem.add(bev_flex)
    #
    # bev_fix = BevTech(
    #     type="bev",
    #     label="BEV-G2V",
    #     electricity_bus=el_bus,
    #     commodity_bus=indiv_mob,
    #     storage_capacity=200,
    #     drive_power=100,
    #     # drive_consumption=[0, 1, 0],
    #     charging_power=200,
    #     availability=len(periods) * [1, 1, 1],
    #     v2g=False,
    #     # loss_rate=0.01,
    #     # min_storage_level=[0.1, 0.2, 0.15, 0.15],
    #     # max_storage_level=[0.9, 0.95, 0.92, 0.92],
    #     expandable=True,
    #     bev_invest_costs=2,
    #     invest_c_rate=60 / 20,  # Capacity/Power
    #     variable_costs=3,
    #     fixed_investment_costs=1,
    #     commodity_conversion_rate=0.7,
    #     input_parameters={
    #         "fix": len(periods) * [0, 0, 0]
    #     },  # fixed relative charging profile
    #     lifetime=10,
    # )
    # energysystem.add(bev_fix)

    bevfleet = BevFleet(
        label="BEV",
        electricity_bus=el_bus,
        demand_bus=indiv_mob,
        charging_power_flex=200,
        charging_power_inflex=150,
        minimum_charging_power_investment=0,
        maximum_charging_power_investment=1000,
        availability_flex=[0.8] * len(date_time_index),
        availability_inflex=[0.8] * len(date_time_index),
        # storage_capacity=50,
        min_storage_level=[0] * len(date_time_index),
        max_storage_level=[0] * len(date_time_index),
        # drive_power: int = 0,
        # drive_consumption: Sequence[float] = None
        loss_rate=0.1,
        efficiency_mob_g2v=[1] * len(date_time_index),
        efficiency_mob_v2g=[1] * len(date_time_index),
        efficiency_sto_in=[1] * len(date_time_index),
        efficiency_sto_out=[1] * len(date_time_index),
        # efficiency_mob_electrical=1,#[1]*len(date_time_index),
        commodity_conversion_rate=[1] * len(date_time_index),
        expandable=False,
        lifetime=20,
        age=0,
        invest_c_rate=60 / 20,
        bev_invest_costs=[5] * len(periods),
        fixed_costs=[10]
        * len(
            [2020, 2030]
        ),  # eigentlich für jedes explizite und implizite Jahr
        fixed_investment_costs=[20] * len(periods),
        variable_costs=[2] * len(date_time_index),
        balanced=True,
        input_parameters_inflex={"fix": len(periods) * [0, 0, 0]},
        # output_parameters: dict = field(default_factory=dict)
    )

    energysystem.add(bevfleet)

    mp.draw_graph(energysystem)

    print("test")
    # model = solph.Model(
    #     energysystem,
    #     timeindex=energysystem.timeindex,
    # )
    #
    # filepath = "./mobility.lp"
    # model.write(filepath, io_options={"symbolic_solver_labels": True})
    #
    # datapackage_dir = os.path.join(
    #     tabular_path[0], "examples/own_examples/bev"
    # )
    # deserialize_constraints(
    #     model=model,
    #     path=os.path.join(datapackage_dir, "datapackage.json"),
    #     constraint_type_map=CONSTRAINT_TYPE_MAP,
    # )
    #
    # filepath = "./mobility_constrained.lp"
    # model.write(filepath, io_options={"symbolic_solver_labels": True})
    #
    # # select solver 'gurobi', 'cplex', 'glpk' etc
    # model.solve("cbc", solve_kwargs={"tee": True})
    # # model.display()
    #
    # energysystem.params = solph.processing.parameter_as_dict(
    #     energysystem, exclude_attrs=["subnodes"]
    # )
    # energysystem.results = model.results()
    #
    # # Rename results for easy access
    # energysystem.new_results = {}
    # for r in energysystem.results:
    #     if r[1] is not None:
    #         energysystem.new_results[f"{r[0].label}: {r[1].label}"] = (
    #             energysystem.results[r]
    #         )
    #
    # # postprocessing
    # postprocessed_results = calculations.run_postprocessing(energysystem)
    #
    # # # plot bev results
    # # mp.plot_bev_results(
    # #     energysystem=energysystem,
    # #     facade_label=["BEV-V2G", "BEV-FLEX"]
    # # )
    #
    # print(postprocessed_results)
