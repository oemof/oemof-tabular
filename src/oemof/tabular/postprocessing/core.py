import abc
import inspect
import logging
from dataclasses import dataclass
from typing import Dict, Optional, Type, Union

import pandas as pd


class CalculationError(Exception):
    """Raised if something is wrong in calculation"""


@dataclass
class ParametrizedCalculation:
    calculation: Type["Calculation"]
    parameters: Optional[dict] = None


def get_dependency_name(
    calculation: Union[
        "Calculation", Type["Calculation"], ParametrizedCalculation
    ]
):
    if isinstance(calculation, Calculation):
        # Get name from instance
        signiture = inspect.signature(calculation.__init__)
        return "_".join(
            [calculation.name]
            + [
                f"{parameter}={getattr(calculation, parameter)}"
                for parameter in signiture.parameters
                if parameter not in ("self", "calculator")
            ]
        )
    # Get name from class and default parameters in class
    if isinstance(calculation, ParametrizedCalculation):
        calc = calculation.calculation
        parameters = calculation.parameters or {}
    else:
        calc = calculation
        parameters = {}
    signiture = inspect.signature(calc.__init__)
    names = [calc.name]
    for name, sig_parameter in signiture.parameters.items():
        if name not in ("self", "calculator"):
            value = parameters.get(name)
            if value:
                names.append(f"{name}={value}")
                continue
            if sig_parameter.default is inspect.Parameter.empty:
                raise CalculationError(
                    f"Parameter '{name}' in calculation '{calc.name}' not set."
                )
            names.append(f"{name}={sig_parameter.default}")
    return "_".join(names)


class Calculator:
    """Entity to gather calculations and their results"""

    def __init__(self, input_parameters, output_parameters):
        self.calculations = {}
        self.is_multi_period = (
            "period_scalars" in list(output_parameters.values())[0]
        )
        self.scalar_params = self.__init_df(input_parameters, "scalars")
        self.scalars = self.__init_df(output_parameters, "scalars")
        self.sequences_params = self.__init_df(input_parameters, "sequences")
        self.sequences = self.__init_df(output_parameters, "sequences")
        self.busses = self.__filter_type("bus")
        self.links = self.__filter_type("link")
        logging.info("Successfully set up calculator")

    def __init_df(self, oemof_data, data_type="scalars"):
        r"""
        Converts scalars/sequences dictionary to a multi-indexed
        DataFrame.
        """

        def convert_to_pandas(value):
            if data_key in ("sequences", "period_scalars"):
                result_type = pd.DataFrame
            else:
                result_type = pd.Series

            if isinstance(value[data_key], result_type):
                return value[data_key]
            if data_key in ("sequences", "period_scalars"):
                return pd.DataFrame.from_dict(value[data_key], dtype="object")
            return pd.Series(value[data_key], dtype="object")

        data_key = (
            "period_scalars"
            if "period_scalars" in list(oemof_data.values())[0]
            and data_type == "scalars"
            else data_type
        )
        data = {
            tuple(
                str(k) if k is not None else None for k in key
            ): convert_to_pandas(value)
            for key, value in oemof_data.items()
        }
        results = []
        for key, series in data.items():
            if series.empty:
                continue
            if data_key == "period_scalars":
                series = series.transpose()
            mindex = pd.MultiIndex.from_tuples(
                [
                    (*key, entry)
                    for entry in (
                        series.index
                        if data_type == "scalars"
                        else series.columns
                    )
                ],
                names=["source", "target", "var_name"],
            )
            if data_type == "scalars":
                series.index = mindex
            else:
                series.columns = mindex
            results.append(series)
        if results:
            return pd.concat(
                results, axis=(0 if data_type == "scalars" else 1)
            )
        return (
            pd.Series(dtype="object")
            if data_type == "scalars"
            else pd.DataFrame(dtype="object")
        )

    def __filter_type(self, type_: str):
        return tuple(
            self.scalar_params[:, :, "type"][
                self.scalar_params[:, :, "type"] == type_
            ].index.get_level_values(0)
        )

    def add(
        self,
        calculation: Union[
            "Calculation", Type["Calculation"], ParametrizedCalculation
        ],
    ):
        """Adds calculation to calculations 'tree' if not yet present"""
        dependency_name = get_dependency_name(calculation)
        if isinstance(calculation, Calculation):
            if dependency_name in self.calculations:
                raise CalculationError(
                    f"Calculation '{calculation.__class__.__name__}' "
                    f"already exists in calculator"
                )
            self.calculations[dependency_name] = calculation
            return
        if dependency_name in self.calculations:
            return
        if isinstance(calculation, ParametrizedCalculation):
            if calculation.parameters:
                self.calculations[dependency_name] = calculation.calculation(
                    self, **calculation.parameters
                )
            else:
                self.calculations[dependency_name] = calculation.calculation(
                    self
                )
            return
        if issubclass(calculation, Calculation):
            self.calculations[dependency_name] = calculation(self)
            return
        raise CalculationError("Can only add Calculation instances or classes")

    def get_result(self, dependency_name):
        """Returns result of given dependency"""
        if dependency_name not in self.calculations:
            raise KeyError(
                f"Could not find calculation named '{dependency_name}'."
            )
        return self.calculations[dependency_name].result


class Calculation(abc.ABC):
    """
    Abstract class for calculations

    Dependent calculations are defined in `depends_on` either as subclass of
    `Calculation` or as instance of `ParametrizedCalculation`
    (if calculation needs parameters) and automatically added to calculation
    'tree' if not yet present. Function `calculate_result` is abstract and must
    be implemented by child class.
    """

    name = None
    parameters = ()
    depends_on: Dict[str, Union["Calculation", ParametrizedCalculation]] = None

    def __init__(self, calculator: Calculator):
        super(Calculation, self).__init__()
        self.calculator = calculator
        self.calculator.add(self)
        self.__add_dependencies()
        self.__result = None

    def __add_dependencies(self):
        if not self.depends_on:
            return
        for dependency in self.depends_on.values():
            self.calculator.add(dependency)

    def dependency(self, name):
        dependency_name = get_dependency_name(self.depends_on[name])
        return self.calculator.get_result(dependency_name)

    @abc.abstractmethod
    def calculate_result(self):
        """This method must be implemented in child class"""

    @property
    def result(self):
        if self.__result is None:
            self.__result = self.calculate_result()
        return self.__result

    @property
    def scalar_params(self):
        return self.calculator.scalar_params

    @property
    def scalars(self):
        return self.calculator.scalars

    @property
    def sequences_params(self):
        return self.calculator.sequences_params

    @property
    def sequences(self):
        return self.calculator.sequences

    @property
    def busses(self):
        return self.calculator.busses

    @property
    def links(self):
        return self.calculator.links
