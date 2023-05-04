import pathlib
from unittest import mock

import pandas
import pytest

from oemof.tabular import datapackage  # noqa: F401
from oemof.tabular.postprocessing import calculations, core

TEST_FILES_DIR = pathlib.Path(__file__).parent / "_files"


class ParametrizedCalculation(core.Calculation):
    name = "pc"

    def __init__(self, calculator, a, b=4):
        self.a = a
        self.b = b
        super().__init__(calculator)

    def calculate_result(self):
        return


def test_dependency_name():
    calculator = mock.MagicMock()
    summed_flows = calculations.AggregatedFlows(calculator)
    name = core.get_dependency_name(summed_flows)
    assert name == (
        "aggregated_flows_from_nodes=None_to_nodes=None_"
        "resample_mode=None_drop_component_to_component=True"
    )

    dep = core.ParametrizedCalculation(calculations.AggregatedFlows)
    name = core.get_dependency_name(dep)
    assert name == (
        "aggregated_flows_from_nodes=None_to_nodes=None_"
        "resample_mode=None_drop_component_to_component=True"
    )

    name = core.get_dependency_name(
        ParametrizedCalculation(calculator, a=2, b=2)
    )
    assert name == "pc_a=2_b=2"

    name = core.get_dependency_name(ParametrizedCalculation(calculator, a=2))
    assert name == "pc_a=2_b=4"

    dep = core.ParametrizedCalculation(ParametrizedCalculation)
    with pytest.raises(core.CalculationError):
        core.get_dependency_name(dep)

    dep = core.ParametrizedCalculation(
        ParametrizedCalculation, {"a": 2, "b": 6}
    )
    name = core.get_dependency_name(dep)
    assert name == "pc_a=2_b=6"

    dep = core.ParametrizedCalculation(ParametrizedCalculation, {"a": 2})
    name = core.get_dependency_name(dep)
    assert name == "pc_a=2_b=4"


def test_aggregated_flows_calculation():
    params = {
        ("a", "b"): {
            "scalars": pandas.Series(["bus"], ["type"]),
            "sequences": pandas.DataFrame(),
        }
    }
    results = {
        ("process_1", "a"): {
            "scalars": pandas.Series(),
            "sequences": pandas.DataFrame(
                index=pandas.date_range("01-01-2019", "01-05-2019", freq="d"),
                data={"flow": range(5)},
            ),
        },
        ("process_2", "a"): {
            "scalars": pandas.Series(),
            "sequences": pandas.DataFrame(
                index=pandas.date_range("01-01-2019", "01-05-2019", freq="d"),
                data={"flow": range(5)},
            ),
        },
    }
    calculator = core.Calculator(params, results)
    agg = calculations.AggregatedFlows(calculator, resample_mode="M")
    agg2 = calculations.AggregatedFlows(
        calculator, resample_mode="D", from_nodes=["process_1"]
    )
    assert len(agg.result) == 1
    assert len(agg.result.columns) == 2
    assert len(agg2.result) == 5
    assert len(agg2.result.columns) == 1
