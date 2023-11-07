import logging

import pandas as pd
from oemof.solph import helpers

from oemof import solph
from oemof.tabular.constraint_facades import BevEqualInvest, BevShareMob
from oemof.tabular.facades import Bev, Excess, Load, Shortage, Volatile
from oemof.tabular.postprocessing import calculations


class TestFacades:
    @classmethod
    def setup_class(cls):
        cls.date_time_index = pd.date_range("1/1/2020", periods=3, freq="H")

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
            capacity=100,
            profile=[1, 0, 0],
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=50,
            profile=[0, 1, 0],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=50,  # PKM
            profile=[0, 0, 1],  # drive consumption
        )

        self.energysystem.add(pkm_demand)

        bev_v2g = Bev(
            type="bev",
            label="BEV-V2G",
            v2g=True,
            electricity_bus=el_bus,
            transport_commodity_bus=indiv_mob,
            storage_capacity=200,
            capacity=200,  # TODO replace by storage_capacity
            loss_rate=0,
            max_charging_power=50,
            availability=[1, 1, 1],
            # min_storage_level=[0.1, 0.2, 0.15, 0.15],
            # max_storage_level=[0.9, 0.95, 0.92, 0.92],
            efficiency_charging=1,
            pkm_conversion_rate=1,
            efficiency_mob_g2v=1,
            efficiency_mob_v2g=1,
            efficiency_mob_electrical=1,
            efficiency_sto_in=1,
            efficiency_sto_out=1,
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
        assert self.results[cn]["sequences"]["storage_content"].iloc[1] == 100
        assert self.results[cn]["sequences"]["storage_content"].iloc[2] == 50
        assert self.results[cn]["sequences"]["storage_content"].iloc[3] == 0
