import logging

import pandas as pd
from oemof.solph import helpers

from oemof import solph

# from oemof.tabular.constraint_facades import BevEqualInvest, BevShareMob
from oemof.tabular.facades import Bev, Load, Volatile  # , Shortage, Excess

# from oemof.tabular.postprocessing import calculations


class TestFacades:
    @classmethod
    def setup_class(cls):
        cls.date_time_index = pd.date_range("1/1/2020", periods=4, freq="H")

        cls.tmpdir = helpers.extend_basic_path("tmp")
        logging.info(cls.tmpdir)

    @classmethod
    def setup_method(cls):
        cls.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS, timeindex=cls.date_time_index
        )

    def get_om(self):
        self.model = solph.Model(
            self.energysystem,
            timeindex=self.energysystem.timeindex,
        )

    def solve_om(self):
        opt_result = self.model.solve("cbc", solve_kwargs={"tee": True})
        self.results = self.model.results()
        return opt_result

    def rename_results(self):
        rename_mapping = {
            oemof_tuple: f"{oemof_tuple[0]}->{oemof_tuple[1]}"
            for oemof_tuple in self.results.keys()
        }
        for old_key, new_key in rename_mapping.items():
            self.results[new_key] = self.results.pop(old_key)

    def test_bev_v2g_dispatch(self):
        el_bus = solph.Bus("el-bus")
        el_bus.type = "bus"
        self.energysystem.add(el_bus)

        indiv_mob = solph.Bus("pkm-bus")
        indiv_mob.type = "bus"
        self.energysystem.add(indiv_mob)

        volatile = Volatile(
            label="wind",
            bus=el_bus,
            carrier="wind",
            tech="onshore",
            capacity=495.36,
            profile=[1, 0, 0, 1 / 3],
            variable_costs=10,
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=100,
            profile=[0, 1, 0, 0.1],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=100,  # PKM
            profile=[0, 0, 1, 0.5],  # drive consumption
        )

        self.energysystem.add(pkm_demand)

        bev_v2g = Bev(
            type="bev",
            label="BEV-V2G",
            v2g=True,
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=500,
            loss_rate=0,  # self discharge of storage
            charging_power=500,
            availability=[1, 1, 1, 1],  # Vehicle availability at charger
            # min_storage_level=[0.1, 0.2, 0.15, 0.15],
            # max_storage_level=[0.9, 0.95, 0.92, 0.92],
            # efficiency_charging=1,
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_v2g=5 / 6,  # V2G charger efficiency
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=10,  # Charging costs
        )

        self.energysystem.add(bev_v2g)

        # excess = Excess(
        #     type="excess",
        #     label="excess",
        #     bus=el_bus,
        #     carrier="electricity",
        #     tech="excess",
        #     capacity=1e6,
        #     marginal_cost=1e6,
        # )
        # self.energysystem.add(excess)
        #
        # shortage = Shortage(
        #     type="shortage",
        #     label="shortage",
        #     bus=el_bus,
        #     carrier="electricity",
        #     tech="shortage",
        #     capacity=1e6,
        #     marginal_cost=1e6,
        # )
        # self.energysystem.add(shortage)

        self.get_om()

        solver_stats = self.solve_om()

        # TODO check why this is not working
        # self.energysystem.params = solph.processing.parameter_as_dict(
        #     self.energysystem)
        # postprocessed_results = calculations.run_postprocessing(
        #     self.energysystem)

        # rename results to make them accessible
        self.rename_results()

        assert solver_stats["Solver"][0]["Status"] == "ok"

        # Check Storage level
        cn = "BEV-V2G-storage->None"
        assert self.results[cn]["sequences"]["storage_content"].iloc[0] == 0
        assert self.results[cn]["sequences"]["storage_content"].iloc[1] == 344
        assert self.results[cn]["sequences"]["storage_content"].iloc[2] == 200
        assert self.results[cn]["sequences"]["storage_content"].iloc[3] == 27.2
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[4]
            == 48.522222
        )
