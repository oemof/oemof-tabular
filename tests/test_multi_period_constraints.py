import logging
import os
import re
from difflib import unified_diff

import pandas as pd
from oemof.solph import buses, helpers

from oemof import solph
from oemof.tabular.constraint_facades import GenericIntegralLimit
from oemof.tabular.facades import (
    BackpressureTurbine,
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
                else "+"
                if lines[n]
                else lines[n]
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


class TestMultiPeriodConstraints:
    @classmethod
    def setup_class(cls):
        """Setup the test class."""
        cls.objective_pattern = re.compile(
            r"^objective.*(?=s\.t\.)", re.DOTALL | re.MULTILINE
        )

        t_idx_1 = pd.date_range("1/1/2020", periods=3, freq="H")
        t_idx_2 = pd.date_range("1/1/2030", periods=3, freq="H")
        t_idx_3 = pd.date_range("1/1/2040", periods=3, freq="H")

        # Create an overall timeindex
        t_idx_1_series = pd.Series(index=t_idx_1, dtype="float64")
        t_idx_2_series = pd.Series(index=t_idx_2, dtype="float64")
        t_idx_3_series = pd.Series(index=t_idx_3, dtype="float64")

        cls.timeindex = pd.concat(
            [t_idx_1_series, t_idx_2_series, t_idx_3_series]
        ).index
        logging.info(f"Created timeindex with {len(cls.timeindex)} entries.")

        # Create periods
        cls.periods = [t_idx_1, t_idx_2, t_idx_3]
        logging.info(f"Multi-Period approach with {len(cls.periods)} periods.")

        # Create a temporary directory
        cls.tmpdir = helpers.extend_basic_path("tmp")
        logging.info(cls.tmpdir)

    @classmethod
    def setup_method(cls):
        """Setup method which is called before every test"""

        # Create an energy system
        cls.energysystem = solph.EnergySystem(
            groupings=solph.GROUPINGS,
            timeincrement=[1] * len(cls.timeindex),
            periods=cls.periods,
            timeindex=cls.timeindex,
            infer_last_interval=False,
        )

    @classmethod
    def get_om(cls):
        """Create the optimization model from the defined energy system"""
        return solph.Model(
            cls.energysystem,
            timeindex=cls.energysystem.timeindex,
            discount_rate=0.02,
        )

    @classmethod
    def compare_to_reference_lp(cls, ref_filename, my_om=None):
        """Compare the lp file to a reference file"""
        if my_om is None:
            om = cls.get_om()
        else:
            om = my_om

        tmp_filename = ref_filename.replace(".lp", "") + "_tmp.lp"

        new_filepath = os.path.join(cls.tmpdir, tmp_filename)

        om.write(new_filepath, io_options={"symbolic_solver_labels": True})

        ref_filepath = os.path.join(
            os.path.dirname(__file__),
            "_files",
            "lp_files",
            "multi-period",
            ref_filename,
        )

        with open(new_filepath) as new_file:
            with open(ref_filepath) as ref_file:
                compare_lp_files(new_file, ref_file)

    def test_load(self):
        """Test a simple load model"""

        bus_el = buses.Bus("bus_el")

        load = Load(
            label="load",
            carrier="electricity",
            bus=bus_el,
            amount=100,
            profile=[0.3, 0.2, 0.5] * len(self.periods),
        )
        self.energysystem.add(bus_el, load)

        self.compare_to_reference_lp("load_multi_period.lp")

    def test_storage_investment_green_field(self):
        r"""
        Storage investment without existing capacities.
        """
        bus_el = buses.Bus(label="bus_el", balanced=True)

        storage = Storage(
            label="storage",
            carrier="electricity",
            tech="storage",
            bus=bus_el,
            efficiency=0.9,
            expandable=True,
            lifetime=20,
            storage_capacity=0,  # No initial storage capacity
            storage_capacity_potential=10,
            storage_capacity_cost=1300,
            capacity=0,  # No initially installed capacity
            capacity_cost=240,
            capacity_potential=3,
        )
        self.energysystem.add(bus_el, storage)
        self.compare_to_reference_lp(
            "storage_investment_green_field_multi_period.lp"
        )

    def test_storage_investment_brown_field(self):
        r"""
        Storage investment with existing capacities.
        """
        bus_el = buses.Bus(label="bus_el", balanced=True)

        storage = Storage(
            label="storage",
            carrier="electricity",
            tech="storage",
            bus=bus_el,
            efficiency=0.9,
            expandable=True,
            lifetime=20,
            storage_capacity=2,  # Existing initial storage capacity
            storage_capacity_potential=10,
            storage_capacity_cost=1300,
            capacity=1,  # Existing capacity
            capacity_cost=240,
            capacity_potential=5,
        )
        self.energysystem.add(bus_el, storage)
        self.compare_to_reference_lp(
            "storage_investment_brown_field_multi_period.lp"
        )

    def test_storage_investment_brown_field_no_storage_capacity_cost(self):
        r"""
        Storage investment with existing capacities. No costs for storage
        capacity (units of energy).
        """
        bus_el = buses.Bus(label="bus_el", balanced=True)

        storage = Storage(
            label="storage",
            carrier="electricity",
            tech="storage",
            bus=bus_el,
            efficiency=0.9,
            expandable=True,
            lifetime=20,
            storage_capacity=2,  # Existing initial storage capacity
            storage_capacity_potential=10,
            capacity=1,  # Existing capacity
            capacity_cost=240,
            capacity_potential=5,
        )
        self.energysystem.add(bus_el, storage)
        self.compare_to_reference_lp(
            "storage_investment_brown_field_no_storage_capacity_cost"
            "_multi_period.lp"
        )

    def test_backpressure_investment_green_field(self):
        r"""
        BackpressureTurbine investment without existing capacities.
        """
        bus_fuel = buses.Bus(label="bus_fuel", balanced=True)
        bus_el = buses.Bus(label="bus_el", balanced=True)
        bus_heat = buses.Bus(label="bus_heat", balanced=True)

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
            lifetime=20,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, bpchp)
        self.compare_to_reference_lp(
            "backpressure_investment_green_field_multi_period.lp"
        )

    def test_backpressure_investment_brown_field(self):
        r"""
        BackpressureTurbine investment with existing capacities.
        """
        bus_fuel = solph.Bus(label="fuel", balanced=True)
        bus_el = solph.Bus(label="electricity", balanced=True)
        bus_heat = solph.Bus(label="heat", balanced=True)

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
            lifetime=20,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, bpchp)
        self.compare_to_reference_lp(
            "backpressure_investment_brown_field_multi_period.lp"
        )

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
            lifetime=20,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, extchp)
        self.compare_to_reference_lp(
            "extraction_investment_green_field_multi_period.lp"
        )

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
            lifetime=20,
        )
        self.energysystem.add(bus_el, bus_fuel, bus_heat, extchp)
        self.compare_to_reference_lp(
            "extraction_investment_brown_field_multi_period.lp"
        )

    def test_commodity(self):
        r""" """
        bus_biomass = solph.Bus("biomass")

        commodity = Commodity(
            label="biomass-commodity",
            bus=bus_biomass,
            carrier="biomass",
            amount=1000,
            marginal_cost=10,
            output_parameters={"max": [0.9, 0.5, 0.4] * len(self.periods)},
        )
        self.energysystem.add(bus_biomass, commodity)
        self.compare_to_reference_lp("commodity_multi_period.lp")

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
        self.compare_to_reference_lp("conversion_multi_period.lp")

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
        self.compare_to_reference_lp("dispatchable_multi_period.lp")

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

        self.compare_to_reference_lp("excess_multi_period.lp")

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
        self.compare_to_reference_lp("link_multi_period.lp")

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
            profile=[1, 2, 6] * len(self.periods),
            loss_rate=0.1,
            initial_storage_level=0,
            max_storage_level=0.75,
            efficiency=0.8,
        )
        self.energysystem.add(bus, reservoir)
        self.compare_to_reference_lp("reservoir_multi_period.lp")

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
            max_storage_level=[0.75, 0.5, 0.25] * len(self.periods),
            expandable=True,
            lifetime=20,
        )
        self.energysystem.add(bus, storage)
        self.compare_to_reference_lp("storage_multi_period.lp")

    def test_volatile(self):
        # Create buses
        bus_el = buses.Bus(label="bus_el", balanced=True)

        # Create components
        volatile = Volatile(
            label="wind",
            bus=bus_el,
            carrier="wind",
            tech="onshore",
            capacity=10,
            capacity_cost=150,
            expandable=True,
            capacity_potential=100,
            profile=[0.25, 0.1, 0.3] * len(self.periods),
            lifetime=5,
        )

        self.energysystem.add(bus_el, volatile)
        self.compare_to_reference_lp("volatile_multi_period.lp")

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

        emission_constraint = GenericIntegralLimit(
            name="emission_constraint",
            type="e",
            limit=1000,
        )

        self.energysystem.add(bus, dispatchable)

        model = solph.Model(self.energysystem)

        emission_constraint.build_constraint(model)

        self.compare_to_reference_lp(
            "emission_constraint_multi_period.lp", my_om=model
        )
