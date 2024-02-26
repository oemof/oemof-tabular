import logging
import os
import re
from difflib import unified_diff

import pandas as pd
from oemof.solph import helpers

from oemof import solph
from oemof.tabular.constraint_facades import CONSTRAINT_TYPE_MAP
from oemof.tabular.facades import (
    BackpressureTurbine,
    Bev,
    Commodity,
    Conversion,
    Dispatchable,
    Excess,
    ExtractionTurbine,
    Link,
    Load,
    Reservoir,
    Storage,
    Volatile,
)


def chop_trailing_whitespace(lines):
    return [re.sub(r"\s*$", "", line) for line in lines]


def remove(pattern, lines):
    if not pattern:
        return lines
    return re.subn(pattern, "", "\n".join(lines))[0].split("\n")


def normalize_to_positive_results(lines):
    negative_result_indices = [
        n for n, line in enumerate(lines) if re.match("^= -", line)
    ]
    equation_start_indices = [
        [n for n in reversed(range(0, nri)) if re.match(".*:$", lines[n])][0]
        + 1
        for nri in negative_result_indices
    ]
    for start, end in zip(equation_start_indices, negative_result_indices):
        for n in range(start, end):
            lines[n] = (
                "-"
                if lines[n] and lines[n][0] == "+"
                else "+" if lines[n] else lines[n]
            ) + lines[n][1:]
        lines[end] = "= " + lines[end][3:]
    return lines


def compare_lp_files(lp_file_1, lp_file_2, ignored=None):
    lines_1 = remove(ignored, chop_trailing_whitespace(lp_file_1.readlines()))
    lines_2 = remove(ignored, chop_trailing_whitespace(lp_file_2.readlines()))

    lines_1 = normalize_to_positive_results(lines_1)
    lines_2 = normalize_to_positive_results(lines_2)

    lines_1 = sorted(lines_1)
    lines_2 = sorted(lines_2)

    assert len(lines_1) == len(lines_2)

    if not lines_1 == lines_2:
        raise AssertionError(
            "Failed matching lp_file_1 with lp_file_2:\n"
            + "\n".join(
                unified_diff(
                    lines_1,
                    lines_2,
                    fromfile=os.path.relpath(lp_file_1.name),
                    tofile=os.path.basename(lp_file_2.name),
                    lineterm="",
                )
            )
        )


class TestConstraints:
    @classmethod
    def setup_class(cls):
        cls.objective_pattern = re.compile(
            r"^objective.*(?=s\.t\.)", re.DOTALL | re.MULTILINE
        )

        cls.date_time_index = pd.date_range("1/1/2012", periods=3, freq="H")

        cls.tmpdir = helpers.extend_basic_path("tmp")
        logging.info(cls.tmpdir)

    @classmethod
    def setup_method(cls):
        cls.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS, timeindex=cls.date_time_index
        )

    def get_om(self):
        return solph.Model(
            self.energysystem,
            timeindex=self.energysystem.timeindex,
        )

    def compare_to_reference_lp(self, ref_filename, my_om=None):
        if my_om is None:
            om = self.get_om()
        else:
            om = my_om

        tmp_filename = ref_filename.replace(".lp", "") + "_tmp.lp"

        new_filepath = os.path.join(self.tmpdir, tmp_filename)

        om.write(new_filepath, io_options={"symbolic_solver_labels": True})

        ref_filepath = os.path.join(
            os.path.dirname(__file__), "_files", "lp_files", ref_filename
        )

        with open(new_filepath) as new_file:
            with open(ref_filepath) as ref_file:
                compare_lp_files(new_file, ref_file)

    def test_storage_investment_green_field(self):
        r"""
        Storage investment without existing capacities.
        """
        el_bus = solph.Bus(label="electricity")

        storage = Storage(
            label="storage",
            carrier="electricity",
            tech="storage",
            bus=el_bus,
            efficiency=0.9,
            expandable=True,
            storage_capacity=0,  # No initially installed storage capacity
            storage_capacity_potential=10,
            storage_capacity_cost=1300,
            capacity=0,  # No initially installed capacity
            capacity_cost=240,
            capacity_potential=3,
        )
        self.energysystem.add(el_bus, storage)

        self.compare_to_reference_lp("storage_investment_green_field.lp")

    def test_storage_investment_brown_field(self):
        r"""
        Storage investment with existing capacities.
        """
        bus_el = solph.Bus(label="electricity")

        storage = Storage(
            label="storage",
            carrier="electricity",
            tech="storage",
            bus=bus_el,
            efficiency=0.9,
            expandable=True,
            storage_capacity=2,  # Existing storage capacity
            storage_capacity_potential=10,
            storage_capacity_cost=1300,
            capacity=1,  # Existing capacity
            capacity_cost=240,
            capacity_potential=5,
        )
        self.energysystem.add(bus_el, storage)

        self.compare_to_reference_lp("storage_investment_brown_field.lp")

    def test_storage_investment_brown_field_no_storage_capacity_cost(self):
        r"""
        Storage investment with existing capacities. No costs for storage
        capacity (units of energy).
        """
        bus_el = solph.Bus(label="electricity")

        storage = Storage(
            label="storage",
            carrier="electricity",
            tech="storage",
            bus=bus_el,
            efficiency=0.9,
            expandable=True,
            storage_capacity=2,  # Existing storage capacity
            storage_capacity_potential=10,
            capacity=1,  # Existing capacity
            capacity_cost=240,
            capacity_potential=5,
        )
        self.energysystem.add(bus_el, storage)

        self.compare_to_reference_lp(
            "storage_investment_brown_field_no_storage_capacity_cost.lp"
        )

    def test_backpressure_investment_green_field(self):
        r"""
        BackpressureTurbine investment without existing capacities.
        """
        bus_fuel = solph.Bus(label="fuel")
        bus_el = solph.Bus(label="electricity")
        bus_heat = solph.Bus(label="heat")

        bpchp = BackpressureTurbine(
            label="backpressure",
            carrier="gas",
            tech="bp",
            fuel_bus=bus_fuel,
            heat_bus=bus_heat,
            electricity_bus=bus_el,
            capacity=0,
            capacity_cost=50,
            carrier_cost=0.6,
            electric_efficiency=0.4,
            thermal_efficiency=0.35,
            expandable=True,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, bpchp)

        self.compare_to_reference_lp("backpressure_investment_green_field.lp")

    def test_backpressure_investment_brown_field(self):
        r"""
        BackpressureTurbine investment with existing capacities.
        """
        bus_fuel = solph.Bus(label="fuel")
        bus_el = solph.Bus(label="electricity")
        bus_heat = solph.Bus(label="heat")

        bpchp = BackpressureTurbine(
            label="backpressure",
            carrier="gas",
            tech="bp",
            fuel_bus=bus_fuel,
            heat_bus=bus_heat,
            electricity_bus=bus_el,
            capacity=1000,
            capacity_cost=50,
            carrier_cost=0.6,
            electric_efficiency=0.4,
            thermal_efficiency=0.35,
            expandable=True,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, bpchp)

        self.compare_to_reference_lp("backpressure_investment_brown_field.lp")

    def test_extraction_investment_green_field(self):
        r"""
        ExtractionTurbine investment without existing capacities.
        """
        bus_fuel = solph.Bus(label="gas")
        bus_el = solph.Bus(label="electricity")
        bus_heat = solph.Bus(label="heat")

        extchp = ExtractionTurbine(
            label="extraction",
            carrier="gas",
            tech="extraction",
            fuel_bus=bus_fuel,
            heat_bus=bus_heat,
            electricity_bus=bus_el,
            capacity=0,
            capacity_cost=50,
            carrier_cost=0.6,
            condensing_efficiency=0.5,
            electric_efficiency=0.4,
            thermal_efficiency=0.35,
            expandable=True,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, extchp)

        self.compare_to_reference_lp("extraction_investment_green_field.lp")

    def test_extraction_investment_brown_field(self):
        r"""
        ExtractionTurbine investment with existing capacities.
        """
        bus_fuel = solph.Bus(label="gas")
        bus_el = solph.Bus(label="electricity")
        bus_heat = solph.Bus(label="heat")

        extchp = ExtractionTurbine(
            label="extraction",
            carrier="gas",
            tech="extraction",
            fuel_bus=bus_fuel,
            heat_bus=bus_heat,
            electricity_bus=bus_el,
            capacity=1000,
            capacity_cost=50,
            carrier_cost=0.6,
            condensing_efficiency=0.5,
            electric_efficiency=0.4,
            thermal_efficiency=0.35,
            expandable=True,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, extchp)

        self.compare_to_reference_lp("extraction_investment_brown_field.lp")

    def test_commodity(self):
        r""" """
        bus_biomass = solph.Bus("biomass")

        commodity = Commodity(
            label="biomass-commodity",
            bus=bus_biomass,
            carrier="biomass",
            amount=1000,
            marginal_cost=10,
            output_parameters={"max": [0.9, 0.5, 0.4]},
        )
        self.energysystem.add(bus_biomass, commodity)

        self.compare_to_reference_lp("commodity.lp")

    def test_conversion(self):
        r""" """
        bus_biomass = solph.Bus("biomass")
        bus_heat = solph.Bus("heat")

        conversion = Conversion(
            label="biomass_plant",
            carrier="biomass",
            tech="st",
            from_bus=bus_biomass,
            to_bus=bus_heat,
            capacity=100,
            efficiency=0.4,
        )
        self.energysystem.add(bus_heat, bus_biomass, conversion)

        self.compare_to_reference_lp("conversion.lp")

    def test_dispatchable(self):
        bus = solph.Bus("electricity")

        dispatchable = Dispatchable(
            label="gt",
            bus=bus,
            carrier="gas",
            tech="ccgt",
            capacity=1000,
            marginal_cost=10,
            output_parameters={"min": 0.2},
        )
        self.energysystem.add(bus, dispatchable)

        self.compare_to_reference_lp("dispatchable.lp")

    def test_excess(self):
        bus = solph.Bus("electricity")

        excess = Excess(
            label="excess",
            bus=bus,
            carrier="electricity",
            tech="excess",
            capacity=1000,
            marginal_cost=10,
        )
        self.energysystem.add(bus, excess)

        self.compare_to_reference_lp("excess.lp")

    def test_link(self):
        r""" """
        bus1 = solph.Bus("bus1")
        bus2 = solph.Bus("bus2")

        link = Link(
            label="link",
            carrier="electricity",
            from_bus=bus1,
            to_bus=bus2,
            from_to_capacity=100,
            to_from_capacity=80,
            loss=0.25,
            marginal_cost=4,
        )
        self.energysystem.add(bus1, bus2, link)

        self.compare_to_reference_lp("link.lp")

    def test_load(self):
        r""" """
        bus = solph.Bus("electricity")

        load = Load(
            label="load",
            carrier="electricity",
            bus=bus,
            amount=100,
            profile=[0.3, 0.2, 0.5],
        )
        self.energysystem.add(bus, load)

        self.compare_to_reference_lp("load.lp")

    def test_reservoir(self):
        r""" """
        bus = solph.Bus("electricity")

        reservoir = Reservoir(
            label="reservoir",
            bus=bus,
            carrier="water",
            tech="reservoir",
            storage_capacity=1000,
            capacity=50,
            profile=[1, 2, 6],
            loss_rate=0.1,
            initial_storage_level=0,
            max_storage_level=0.75,
            efficiency=0.8,
        )
        self.energysystem.add(bus, reservoir)

        self.compare_to_reference_lp("reservoir.lp")

    def test_storage(self):
        r""" """
        bus = solph.Bus("electricity")

        storage = Storage(
            label="storage",
            bus=bus,
            carrier="lithium",
            tech="battery",
            storage_capacity_cost=10,
            invest_relation_output_capacity=1 / 8,  # oemof.solph
            marginal_cost=5,
            balanced=True,  # oemof.solph argument
            initial_storage_level=0.5,  # oemof.solph argument
            max_storage_level=[0.75, 0.5, 0.25],
            expandable=True,
        )
        self.energysystem.add(bus, storage)

        self.compare_to_reference_lp("storage.lp")

    def test_volatile(self):
        r""" """
        bus = solph.Bus("electricity")

        volatile = Volatile(
            label="wind",
            bus=bus,
            carrier="wind",
            tech="onshore",
            capacity=10,
            capacity_cost=150,
            expandable=True,
            capacity_potential=100,
            profile=[0.25, 0.1, 0.3],
        )
        self.energysystem.add(bus, volatile)

        self.compare_to_reference_lp("volatile.lp")

    def test_emission_constraint(self):
        bus = solph.Bus("ch4")

        dispatchable = Dispatchable(
            label="ch4-import",
            bus=bus,
            carrier="ch4",
            tech="import",
            capacity=1000,
            output_parameters={"custom_attributes": {"emission_factor": 2.5}},
        )

        emission_constraint = CONSTRAINT_TYPE_MAP["generic_integral_limit"]
        emission_constraint = emission_constraint(
            name="emission_constraint",
            type="e",
            limit=1000,
        )

        self.energysystem.add(bus, dispatchable)

        model = solph.Model(self.energysystem)

        emission_constraint.build_constraint(model)

    def test_bev_trio(self):
        el_bus = solph.Bus("el-bus")
        el_bus.type = "bus"
        self.energysystem.add(el_bus)

        indiv_mob = solph.Bus("pkm-bus")
        indiv_mob.type = "bus"
        self.energysystem.add(indiv_mob)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=indiv_mob,
            amount=200,  # PKM
            profile=[0, 1, 0],  # drive consumption
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
            initial_storage_level=0,
            availability=[1, 1, 1, 1],  # Vehicle availability at charger
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

        bev_flex = Bev(
            type="bev",
            label="BEV-inflex",
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=0,
            loss_rate=0,  # self discharge of storage
            charging_power=0,
            availability=[1, 1, 1, 1],
            v2g=False,
            balanced=True,
            expandable=True,
            initial_storage_level=0,
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
            bev_invest_costs=2,
            invest_c_rate=60 / 20,  # Capacity/Power
            fixed_investment_costs=1,
            lifetime=10,
        )
        self.energysystem.add(bev_flex)

        bev_fix = Bev(
            type="bev",
            label="BEV-G2V",
            electricity_bus=el_bus,
            commodity_bus=indiv_mob,
            storage_capacity=0,
            loss_rate=0,  # self discharge of storage
            charging_power=0,
            availability=[1, 1, 1, 1],
            v2g=False,
            balanced=True,
            expandable=True,
            initial_storage_level=0,
            commodity_conversion_rate=5 / 6,  # Energy to pkm
            efficiency_mob_electrical=5 / 6,  # Vehicle efficiency per 100km
            efficiency_mob_g2v=5 / 6,  # Charger efficiency
            efficiency_sto_in=5 / 6,  # Storage charging efficiency
            efficiency_sto_out=5 / 6,  # Storage discharging efficiency,
            variable_costs=4,  # Charging costs
            bev_invest_costs=2,
            invest_c_rate=60 / 20,  # Capacity/Power
            fixed_investment_costs=1,
            lifetime=10,
        )
        self.energysystem.add(bev_fix)

        model = solph.Model(self.energysystem)

        year = self.date_time_index.year.min()
        mob_share_constraint = CONSTRAINT_TYPE_MAP["bev_share_mob"]
        mob_share_constraint = mob_share_constraint(
            name=None,
            type=None,
            label="BEV",
            year=year,
            share_mob_flex_V2G=0.3,
            share_mob_inflex=0.2,
            share_mob_flex_G2V=0.5,
        )
        mob_share_constraint.build_constraint(model)

        # these constraints are not mandatory as the energy flow through the
        # facade is already limited by the in & outflow capactiy of the storage
        invest_constraint = CONSTRAINT_TYPE_MAP["bev_equal_invest"]
        invest_constraint = invest_constraint(name=None, type=None, year=year)

        invest_constraint.build_constraint(model)

        self.compare_to_reference_lp("bev_trio_constraint.lp", my_om=model)
