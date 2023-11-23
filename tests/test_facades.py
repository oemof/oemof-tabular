import logging

import pandas as pd
from oemof.solph import helpers

from oemof import solph
from oemof.tabular.constraint_facades import CONSTRAINT_TYPE_MAP
from oemof.tabular.facades import Bev, Load, Volatile  # , Shortage, Excess

# from oemof.tabular.postprocessing import calculations


class TestBevFacadesDispatch:
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
        """
        Tests v2g bev facade in dispatch mode.

        The following energy quantities are used:
        volatile	    +725.76	    0	    0	    0
        load	        0	        -10	    0	    -100
        pkm_demand	    -50	        -50	    -100	0
        V2g storage	    417.6	    316.8	144	    0

        The following efficiencies are taken into consideration:
        volatile --> v2g_storage:   efficiency_sto_in * efficiency_mob_g2v
        storage --> load:           efficiency_sto_out * efficiency_mob_v2g
        storage --> pkm_demand:
            efficiency_sto_out * efficiency_mob_electrical *
                commodity_conversion_rate

        todo, optional: show as table
        """
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
            capacity=725.76,
            profile=[1, 0, 0, 0],
            variable_costs=10,
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=100,
            profile=[0, 0.1, 0, 1],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=100,  # PKM
            profile=[0.5, 0.5, 1, 0],  # drive consumption
        )

        self.energysystem.add(pkm_demand)

        bev_v2g = Bev(
            type="bev",
            label="BEV-V2G",
            v2g=True,
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=800,
            loss_rate=0,  # self discharge of storage
            charging_power=800,
            balanced=True,
            expandable=False,
            initial_storage_capacity=0,
            availability=[1, 1, 1, 1],  # Vehicle availability at charger
            # min_storage_level=[0.0, 0.2, 0.15, 0.0],
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

        self.get_om()

        solver_stats = self.solve_om()

        # rename results to make them accessible
        self.rename_results()

        assert solver_stats["Solver"][0]["Status"] == "ok"

        # Check Storage level
        cn = "BEV-V2G-storage->None"
        assert self.results[cn]["sequences"]["storage_content"].iloc[0] == 0
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[1] == 417.6
        )
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[2] == 316.8
        )
        assert self.results[cn]["sequences"]["storage_content"].iloc[3] == 144
        assert self.results[cn]["sequences"]["storage_content"].iloc[4] == 0

    def test_bev_inflex_dispatch(self):
        """
        Tests inflex bev facade in dispatch mode.

        The following energy quantities are used:
        volatile	    +908.704    0	    0	    0
        load	        -100        0	    0	    0
        pkm_demand	    -100        -50	    -100	-75
        V2g storage	    388.8	    302.4	129.6   0

        The following efficiencies are taken into consideration:
        volatile --> v2g_storage:   efficiency_sto_in * efficiency_mob_g2v
        storage --> load:           efficiency_sto_out * efficiency_mob_v2g
        storage --> pkm_demand:
            efficiency_sto_out * efficiency_mob_electrical *
                commodity_conversion_rate

        todo, optional: show as table
        """
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
            capacity=908.704,
            profile=[1, 0, 0, 0],
            variable_costs=10,
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=100,
            profile=[1, 0, 0, 0],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=100,  # PKM
            profile=[1, 0.5, 1, 0.75],  # drive consumption
        )
        self.energysystem.add(pkm_demand)

        bev_inflex = Bev(
            type="bev",
            label="BEV-inflex",
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=900,
            loss_rate=0,  # self discharge of storage
            charging_power=900,
            # drive_power=100,  # total driving capacity of the fleet
            availability=[1, 1, 1, 1],
            v2g=False,
            # min_storage_level=[0.1, 0.2, 0.15, 0.15],
            # max_storage_level=[0.9, 0.95, 0.92, 0.92],
            balanced=True,
            initial_storage_capacity=0,
            expandable=False,
            input_parameters={
                "fix": [0.89856, 0, 0, 0]
            },  # fixed relative charging profile
            output_parameters={
                "fix": [0.16, 0.08, 0.16, 0.12]
            },  # fixed relative discharging profile
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=8,
        )
        self.energysystem.add(bev_inflex)

        self.get_om()

        solver_stats = self.solve_om()

        # rename results to make them accessible
        self.rename_results()

        assert solver_stats["Solver"][0]["Status"] == "ok"

        # Check Storage level
        cn = "BEV-inflex-storage->None"
        assert self.results[cn]["sequences"]["storage_content"].iloc[0] == 0
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[1] == 388.8
        )
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[2] == 302.4
        )
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[3] == 129.6
        )
        assert self.results[cn]["sequences"]["storage_content"].iloc[4] == 0

    def test_bev_g2v_dispatch(self):
        """
        Tests g2v bev facade in dispatch mode.

        The same quantities as in `test_bev_inflex_dispatch()` are used.
        """
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
            capacity=908.704,
            profile=[1, 0, 0, 0],
            variable_costs=10,
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=100,
            profile=[1, 0, 0, 0],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=100,  # PKM
            profile=[1, 0.5, 1, 0.75],  # drive consumption
        )
        self.energysystem.add(pkm_demand)

        bev_g2v = Bev(
            type="bev",
            label="BEV-G2V",
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=900,
            loss_rate=0,  # self discharge of storage
            charging_power=900,
            # drive_power=100,  # total driving capacity of the fleet
            availability=[1, 1, 1, 1],
            v2g=False,
            # min_storage_level=[0.1, 0.2, 0.15, 0.15],
            # max_storage_level=[0.9, 0.95, 0.92, 0.92],
            balanced=True,
            initial_storage_capacity=0,
            expandable=False,
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=8,
        )
        self.energysystem.add(bev_g2v)

        self.get_om()

        solver_stats = self.solve_om()

        # rename results to make them accessible
        self.rename_results()

        assert solver_stats["Solver"][0]["Status"] == "ok"

        # Check Storage level
        cn = "BEV-G2V-storage->None"
        assert self.results[cn]["sequences"]["storage_content"].iloc[0] == 0
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[1] == 388.8
        )
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[2] == 302.4
        )
        assert (
            self.results[cn]["sequences"]["storage_content"].iloc[3] == 129.6
        )
        assert self.results[cn]["sequences"]["storage_content"].iloc[4] == 0

    def test_bev_trio_dispatch(self):
        """
        Tests linked v2g, g2v and inflex bev facades in dispatch mode.

        Energy quantities are taken from the single tests
        (`test_bev_v2g_dispatch()`, `test_bev_inflex_dispatch()`,
        `test_bev_g2v_dispatch()`) and summed up in this test.

        """
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
            capacity=2543.168,
            profile=[1, 0, 0, 0],
            variable_costs=10,
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=200,
            profile=[1, 0.05, 0, 0.5],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=250,  # PKM
            profile=[1, 0.6, 1.2, 0.6],  # drive consumption
        )
        self.energysystem.add(pkm_demand)

        bev_v2g = Bev(
            type="bev",
            label="BEV-V2G",
            v2g=True,
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=800,
            loss_rate=0,  # self discharge of storage
            charging_power=800,
            balanced=True,
            expandable=False,
            initial_storage_capacity=0,
            availability=[1, 1, 1, 1],  # Vehicle availability at charger
            # min_storage_level=[0.0, 0.2, 0.15, 0.0],
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

        bev_inflex = Bev(
            type="bev",
            label="BEV-inflex",
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=900,
            loss_rate=0,  # self discharge of storage
            charging_power=900,
            # drive_power=100,  # total driving capacity of the fleet
            availability=[1, 1, 1, 1],
            v2g=False,
            # min_storage_level=[0.1, 0.2, 0.15, 0.15],
            # max_storage_level=[0.9, 0.95, 0.92, 0.92],
            balanced=True,
            initial_storage_capacity=0,
            expandable=False,
            input_parameters={
                "fix": [0.89856, 0, 0, 0]
            },  # fixed relative charging profile
            output_parameters={
                "fix": [0.16, 0.08, 0.16, 0.12]
            },  # fixed relative discharging profile
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=20,  # Charging costs
        )
        self.energysystem.add(bev_inflex)

        bev_g2v = Bev(
            type="bev",
            label="BEV-G2V",
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=808.704,
            loss_rate=0,  # self discharge of storage
            charging_power=808.704,
            # drive_power=100,  # total driving capacity of the fleet
            availability=[1, 1, 1, 1],
            v2g=False,
            # min_storage_level=[0.1, 0.2, 0.15, 0.15],
            # max_storage_level=[0.9, 0.95, 0.92, 0.92],
            balanced=True,
            initial_storage_capacity=0,
            expandable=False,
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=4,  # Charging costs
        )
        self.energysystem.add(bev_g2v)

        self.get_om()

        solver_stats = self.solve_om()

        # rename results to make them accessible
        self.rename_results()

        assert solver_stats["Solver"][0]["Status"] == "ok"

        # Check Storage level
        cn = "BEV-V2G-storage->None"
        assert self.results[cn]["sequences"]["storage_content"].iloc[0] == 0
        assert self.results[cn]["sequences"]["storage_content"].iloc[4] == 0

        cn2 = "BEV-inflex-storage->None"
        assert self.results[cn2]["sequences"]["storage_content"].iloc[0] == 0
        assert (
            self.results[cn2]["sequences"]["storage_content"].iloc[1] == 388.8
        )
        assert (
            self.results[cn2]["sequences"]["storage_content"].iloc[2] == 302.4
        )
        assert (
            self.results[cn2]["sequences"]["storage_content"].iloc[3] == 129.6
        )
        assert self.results[cn2]["sequences"]["storage_content"].iloc[4] == 0

        cn3 = "BEV-G2V-storage->None"
        assert self.results[cn3]["sequences"]["storage_content"].iloc[0] == 0
        assert self.results[cn3]["sequences"]["storage_content"].iloc[4] == 0

        # Check storage input flows
        cn4 = "el-bus->BEV-V2G-storage"
        assert self.results[cn4]["sequences"]["flow"].iloc[0] == 725.76

        cn5 = "el-bus->BEV-G2V-storage"
        assert self.results[cn5]["sequences"]["flow"].iloc[0] == 808.704


class TestBevFacadesInvestment:
    @classmethod
    def setup_class(cls):
        t_idx_1 = pd.date_range("1/1/2020", periods=1, freq="H")
        t_idx_2 = pd.date_range("1/1/2030", periods=1, freq="H")
        t_idx_1_series = pd.Series(index=t_idx_1, dtype="float64")
        t_idx_2_series = pd.Series(index=t_idx_2, dtype="float64")
        cls.date_time_index = pd.concat([t_idx_1_series, t_idx_2_series]).index
        cls.periods = [t_idx_1, t_idx_2]

        cls.tmpdir = helpers.extend_basic_path("tmp")
        logging.info(cls.tmpdir)

    @classmethod
    def setup_method(cls):
        cls.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS,
            timeindex=cls.date_time_index,
            infer_last_interval=False,
            timeincrement=[1] * len(cls.date_time_index),
            periods=cls.periods,
        )

    # todo: identical functions can be @fixtures or else (outside of classes)

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

    def test_bev_v2g_invest(self):
        """
        Tests v2g bev facade in investment mode.
        """
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
            capacity=248.832,
            # capacity_cost=1,
            # expandable=True,
            profile=len(self.periods) * [1],
            lifetime=20,
            variable_costs=10,
        )
        self.energysystem.add(volatile)

        load = Load(
            label="load",
            carrier="electricity",
            bus=el_bus,
            amount=0,
            profile=len(self.periods) * [1],
        )
        self.energysystem.add(load)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=100,  # PKM
            profile=len(self.periods) * [1],  # drive consumption
        )
        self.energysystem.add(pkm_demand)

        bev_v2g = Bev(
            type="bev",
            label="BEV-V2G",
            v2g=True,
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=0,
            loss_rate=0,  # self discharge of storage
            charging_power=0,
            balanced=True,
            expandable=True,
            initial_storage_capacity=0,
            availability=len(self.periods)
            * [1],  # Vehicle availability at charger
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_v2g=5 / 6,  # V2G charger efficiency
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=10,  # Charging costs
            bev_invest_costs=2,
            invest_c_rate=60 / 20,  # Capacity/Power
            fixed_investment_costs=1,
            lifetime=10,
        )
        self.energysystem.add(bev_v2g)

        self.get_om()

        for period in self.energysystem.periods:
            year = period.year.min()
            constraint = CONSTRAINT_TYPE_MAP["bev_equal_invest"]
            constraint = constraint(name=None, type=None, year=year)
            # build constraint for each facade & period
            constraint.build_constraint(self.model)

        solver_stats = self.solve_om()

        # rename results to make them accessible
        self.rename_results()

        assert solver_stats["Solver"][0]["Status"] == "ok"

        # Check storage level and invested storage capacity
        cn = "BEV-V2G-storage->None"
        # todo optional capacity as a variable
        # todo 2020 2030 (infer_last_interval missing)
        # todo add second time step to periods
        assert self.results[cn]["sequences"]["storage_content"].iloc[0] == 0
        assert self.results[cn]["sequences"]["storage_content"].iloc[1] == 0
        assert self.results[cn]["period_scalars"]["invest"].iloc[0] == 746.496
        assert self.results[cn]["period_scalars"]["invest"].iloc[1] == 746.496

        # Check invested v2g capacity
        cn2 = "BEV-V2G-v2g->el-bus"
        assert self.results[cn2]["period_scalars"]["invest"].iloc[0] == 248.832
        assert self.results[cn2]["period_scalars"]["invest"].iloc[1] == 248.832

        # Check invested v2g capacity
        cn2 = "BEV-V2G-2com->pkm-bus"
        assert self.results[cn2]["period_scalars"]["invest"].iloc[0] == 248.832
        assert self.results[cn2]["period_scalars"]["invest"].iloc[1] == 248.832


#     This one is only for the bev trio
# ##################################
# for period in self.energysystem.periods:
#     year = period.year.min()
#     constraint = CONSTRAINT_TYPE_MAP["bev_share_mob"]
#     constraint = constraint(
#         name=None,
#         type=None,
#         label="BEV",
#         year=year,
#         share_mob_flex_G2V=0.3,
#         share_mob_flex_V2G=0.2,
#         share_mob_inflex=0.5,
#     )
#     # build constraint for each facade & period
#     constraint.build_constraint(self.model)
