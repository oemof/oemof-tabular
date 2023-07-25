from abc import abstractmethod
from typing import List

import numpy as np
import pandas as pd

from . import core, helper, naming


class AggregatedFlows(core.Calculation):
    name = "aggregated_flows"

    def __init__(
        self,
        calculator: core.Calculator,
        from_nodes: List[str] = None,
        to_nodes: List[str] = None,
        resample_mode: str = None,
        drop_component_to_component: bool = True,
    ):
        if (
            from_nodes
            and to_nodes
            and len(from_nodes) > 1
            and len(to_nodes) > 1
        ):
            raise core.CalculationError(
                "Either 'from_nodes' or 'to_nodes' must contain a single "
                "source/sink."
            )
        self.from_nodes = from_nodes
        self.to_nodes = to_nodes
        self.resample_mode = resample_mode
        self.drop_component_to_component = drop_component_to_component
        super().__init__(calculator)

    def calculate_result(self):
        aggregated_flows = helper.sum_flows(
            self.sequences, resample_mode=self.resample_mode
        )
        axis = 1 if self.resample_mode else 0
        filtered_flows = helper.filter_df_by_input_and_output_nodes(
            aggregated_flows, self.from_nodes, self.to_nodes, axis=axis
        )
        if self.drop_component_to_component:
            filtered_flows = helper.drop_component_to_component(
                filtered_flows, self.busses, axis=axis
            )
        return filtered_flows


class Losses(core.Calculation):
    name = "losses"
    depends_on = {"aggregated_flows": AggregatedFlows}
    var_name = None

    def _calculate_losses(self, aggregated_flows):
        r"""
        Calculate losses within components as the difference of summed input
        to output.
        """
        if not self.var_name:
            raise ValueError("var_name has to be set")
        inputs = helper.get_inputs(aggregated_flows, self.busses)
        outputs = helper.get_outputs(aggregated_flows, self.busses)
        inputs = inputs.groupby("target").sum()
        outputs = outputs.groupby("source").sum()
        losses = inputs - outputs

        # Create MultiIndex:
        losses.index.name = "source"
        losses = losses.reset_index()
        losses["target"] = np.nan
        losses["var_name"] = self.var_name
        losses.set_index(["source", "target", "var_name"], inplace=True)
        return losses[0]  # Return Series instead of DataFrame

    @abstractmethod
    def calculate_result(self):
        raise NotImplementedError


class StorageLosses(Losses):
    name = "storage_losses"
    depends_on = {"aggregated_flows": AggregatedFlows}
    var_name = "storage_losses"

    def calculate_result(self):
        aggregated_flows_storage = helper.filter_series_by_component_attr(
            self.dependency("aggregated_flows"),
            scalar_params=self.scalar_params,
            busses=self.busses,
            type="storage",
        )
        return self._calculate_losses(aggregated_flows_storage)


class TransmissionLosses(Losses):
    name = "transmission_losses"
    depends_on = {"aggregated_flows": AggregatedFlows}
    var_name = "transmission_losses"

    def calculate_result(self):
        aggregated_flows_transmission = helper.filter_series_by_component_attr(
            self.dependency("aggregated_flows"),
            scalar_params=self.scalar_params,
            busses=self.busses,
            type="link",
        )
        return self._calculate_losses(aggregated_flows_transmission)


class Investment(core.Calculation):
    name = "investment"

    def calculate_result(self):
        return (
            pd.Series(dtype="object")
            if (self.scalars is None or self.scalars.empty)
            else helper.filter_by_var_name(self.scalars, "invest")
        )


class EPCosts(core.Calculation):
    name = "ep_costs"

    def calculate_result(self):
        ep_costs = helper.filter_by_var_name(
            self.scalar_params, "investment_ep_costs"
        )
        try:
            return ep_costs.unstack(2)["investment_ep_costs"]
        except KeyError:
            return pd.Series(dtype="object")


class InvestedCapacity(core.Calculation):
    """Collect invested (endogenous) capacity (units of power)"""

    name = "invested_capacity"
    depends_on = {"investment": Investment}

    def calculate_result(self):
        if self.dependency("investment").empty:
            return pd.Series(dtype="object")
        target_is_none = (
            self.dependency("investment").index.get_level_values(1).isnull()
        )
        return self.dependency("investment").loc[~target_is_none]


class InvestedStorageCapacity(core.Calculation):
    """Collect storage capacity (units of energy)"""

    name = "invested_storage_capacity"
    depends_on = {"investment": Investment}

    def calculate_result(self):
        if self.dependency("investment").empty:
            return pd.Series(dtype="object")
        target_is_none = (
            self.dependency("investment").index.get_level_values(1).isnull()
        )
        return self.dependency("investment").loc[target_is_none]


class InvestedCapacityCosts(core.Calculation):
    name = "invested_capacity_costs"
    depends_on = {
        "invested_capacity": InvestedCapacity,
        "ep_costs": EPCosts,
    }

    def calculate_result(self):
        invested_capacity_costs = helper.multiply_var_with_param(
            self.dependency("invested_capacity"), self.dependency("ep_costs")
        )
        if invested_capacity_costs.empty:
            return pd.Series(dtype="object")
        invested_capacity_costs.index = (
            invested_capacity_costs.index.set_levels(
                invested_capacity_costs.index.levels[2] + "_costs", level=2
            )
        )
        return invested_capacity_costs


class InvestedStorageCapacityCosts(core.Calculation):
    name = "invested_storage_capacity_costs"
    depends_on = {
        "invested_storage_capacity": InvestedStorageCapacity,
        "ep_costs": EPCosts,
    }

    def calculate_result(self):
        invested_storage_capacity_costs = helper.multiply_var_with_param(
            self.dependency("invested_storage_capacity"),
            self.dependency("ep_costs"),
        )
        if invested_storage_capacity_costs.empty:
            return pd.Series(dtype="object")
        invested_storage_capacity_costs.index = (
            invested_storage_capacity_costs.index.set_levels(
                invested_storage_capacity_costs.index.levels[2] + "_costs",
                level=2,
            )
        )
        return invested_storage_capacity_costs


class SummedVariableCosts(core.Calculation):
    name = "summed_variable_costs"
    depends_on = {"aggregated_flows": AggregatedFlows}

    def calculate_result(self):
        variable_costs = helper.filter_by_var_name(
            self.scalar_params, "variable_costs"
        ).unstack(2)["variable_costs"]
        variable_costs = variable_costs.loc[variable_costs != 0]
        if variable_costs.empty:
            return pd.Series(dtype="object")
        aggregated_flows = (
            self.dependency("aggregated_flows").unstack(2).loc[:, "flow"]
        )

        summed_variable_costs = helper.multiply_var_with_param(
            aggregated_flows, variable_costs
        )
        summed_variable_costs = helper.set_index_level(
            summed_variable_costs,
            level="var_name",
            value="summed_variable_costs",
        )
        return summed_variable_costs


class SummedCarrierCosts(core.Calculation):
    """
    Calculates summed carrier costs

    An `oemof.tabular` convention: Carrier costs are on inputs,
    marginal costs on output
    """

    name = "summed_carrier_costs"
    depends_on = {"summed_variable_costs": SummedVariableCosts}

    def calculate_result(self):
        return helper.get_inputs(
            self.dependency("summed_variable_costs"), self.busses
        )


class SummedMarginalCosts(core.Calculation):
    """
    Calculates summed marginal costs

    An `oemof.tabular` convention: Carrier costs are on inputs,
    marginal costs on output
    """

    name = "summed_marginal_costs"
    depends_on = {"summed_variable_costs": SummedVariableCosts}

    def calculate_result(self):
        return helper.get_outputs(
            self.dependency("summed_variable_costs"), self.busses
        )


class TotalSystemCosts(core.Calculation):
    name = "total_system_costs"
    depends_on = {
        "invested_capacity_costs": InvestedCapacityCosts,
        "invested_storage_capacity_costs": InvestedStorageCapacityCosts,
        "summed_carrier_costs": SummedCarrierCosts,
        "summed_marginal_costs": SummedMarginalCosts,
    }

    def calculate_result(self):
        all_costs = pd.concat(
            [
                self.dependency("invested_capacity_costs"),
                self.dependency("invested_storage_capacity_costs"),
                self.dependency("summed_carrier_costs"),
                self.dependency("summed_marginal_costs"),
            ]
        )
        index = pd.MultiIndex.from_tuples([("system", "total_system_cost")])
        total_system_cost = pd.DataFrame(
            {"var_value": [all_costs.sum()]}, index=index
        )
        return total_system_cost


def run_postprocessing(es) -> pd.DataFrame:
    # Setup calculations
    calculator = core.Calculator(es.params, es.results)

    aggregated_flows = AggregatedFlows(calculator).result
    storage_losses = StorageLosses(calculator).result
    transmission_losses = TransmissionLosses(calculator).result
    invested_capacity = InvestedCapacity(calculator).result
    invested_storage_capacity = InvestedStorageCapacity(calculator).result
    invested_capacity_costs = InvestedCapacityCosts(calculator).result
    invested_storage_capacity_costs = InvestedStorageCapacityCosts(
        calculator
    ).result
    summed_carrier_costs = SummedCarrierCosts(calculator).result
    summed_marginal_costs = SummedMarginalCosts(calculator).result
    total_system_costs = TotalSystemCosts(calculator).result

    # Combine all results
    all_scalars = [
        aggregated_flows,
        storage_losses,
        transmission_losses,
        invested_capacity,
        invested_storage_capacity,
        invested_capacity_costs,
        invested_storage_capacity_costs,
        summed_carrier_costs,
        summed_marginal_costs,
    ]
    all_scalars = pd.concat(all_scalars, axis=0)
    all_scalars = naming.map_var_names(
        all_scalars,
        calculator.scalar_params,
        calculator.busses,
        calculator.links,
    )
    all_scalars = naming.add_component_info(
        all_scalars, calculator.scalar_params
    )
    total_system_costs.index.names = ("name", "var_name")
    all_scalars = pd.concat([all_scalars, total_system_costs], axis=0)
    all_scalars = all_scalars.sort_values(by=["carrier", "tech", "var_name"])

    return all_scalars
