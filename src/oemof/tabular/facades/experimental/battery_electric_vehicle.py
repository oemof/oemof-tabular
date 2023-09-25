from dataclasses import field
from typing import Sequence, Union

from oemof.solph._plumbing import sequence as solph_sequence
from oemof.solph.buses import Bus
from oemof.solph.components import GenericStorage, Sink, Converter
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Bev(GenericStorage, Facade):
    r"""A fleet of Battery electric vehicles with vehicle-to-grid.

    Note that the investment option is not available for this facade at
    the current development state.

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: int
        The total storage capacity of the vehicles (e.g. in MWh)
    drive_power: int
        Total charging/discharging capacity of the vehicles (e.g. in MW)
    drive_consumption : array-like
        Profile of drive consumption of the fleet (relative to capacity).
    max_charging_power : int
        Max charging/discharging power of all vehicles (e.g. in MW)
    availability : array-like
        Ratio of available capacity for charging/vehicle-to-grid due to
        grid connection.
    efficiency_charging: float
        Efficiency of charging the batteries, default: 1
    v2g: bool
        If True, vehicle-to-grid is enabled, default: False
    loss_rate: float
    min_storage_level : array-like
        Profile of minimum storage level (min SOC)
    max_storage_level : array-like
        Profile of maximum storage level (max SOC).
    balanced : boolean
        Couple storage level of first and last time step.
        (Total inflow and total outflow are balanced.)
    transport_commodity: None
        Bus for the transport commodity
    input_parameters: dict
        Dictionary to specify parameters on the input edge. You can use
        all keys that are available for the  oemof.solph.network.Flow class.
    output_parameters: dict
        see: input_parameters


    The vehicle fleet is modelled as a storage together with an internal
    sink with fixed flow:

    .. math::

        x^{level}(t) =
        x^{level}(t-1) \cdot (1 - c^{loss\_rate}(t))
        + c^{efficiency\_charging}(t) \cdot  x^{flow, in}(t)
        - \frac{x^{drive\_power}(t)}{c^{efficiency\_discharging}(t)}
        - \frac{x^{flow, v2g}(t)}
               {c^{efficiency\_discharging}(t) \cdot c^{efficiency\_v2g}(t)}
        \qquad \forall t \in T

    Note
    ----
    As the Bev is a sub-class of `oemof.solph.GenericStorage` you also
    pass all arguments of this class.

    The concept is similar to the one described in the following publications
    with the difference that uncontrolled charging is not (yet) considered.

    Wulff, N., Steck, F., Gils, H. C., Hoyer-Klick, C., van den Adel,
    B., & Anderson, J. E. (2020).
    Comparing power-system and user-oriented battery electric vehicle
    charging representation and
    its implications on energy system modeling.
    Energies, 13(5). https://doi.org/10.3390/en13051093

    Diego Luca de Tena Costales. (2014).
    Large Scale Renewable Power Integration with Electric Vehicles.
    https://doi.org/10.04.2014

    Examples
    --------
    Basic usage example of the Bev class with an arbitrary selection of
    attributes.

    >>> from oemof import solph
    >>> from oemof.tabular import facades
    >>> my_bus = solph.Bus('my_bus')
    >>> my_bev = Bev(
    ...     label='my_bev',
    ...     bus=el_bus,
    ...     carrier='electricity',
    ...     tech='bev',
    ...     storage_capacity=1000,
    ...     capacity=50,
    ...     availability=[0.8, 0.7, 0.6],
    ...     drive_power=[0.3, 0.2, 0.5],
    ...     amount=450,
    ...     loss_rate=0.01,
    ...     initial_storage_level=0,
    ...     min_storage_level=[0.1, 0.2, 0.15],
    ...     max_storage_level=[0.9, 0.95, 0.92],
    ...     efficiency=0.93
    ...     )

    """

    electricity_bus: Bus

    storage_capacity: int

    drive_power: int

    drive_consumption: Sequence

    max_charging_power: Union[float, Sequence[float]]

    availability: Sequence[float]

    efficiency_charging: float = 1

    v2g: bool = False

    transport_commodity_bus: Bus = None

    input_parameters: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    expandable: bool = False

    def build_solph_components(self):
        facade_label = self.label
        self.label = self.label + "-storage"

        self.nominal_storage_capacity = self.storage_capacity
        # self.inflow_conversion_factor = solph_sequence(1)
        # self.outflow_conversion_factor = solph_sequence(1)
        self.balanced = self.balanced

        if self.expandable:
            raise NotImplementedError(
                "Investment for bev class is not implemented."
            )

        internal_bus = Bus(label=facade_label + "-internal_bus")
        self.bus = internal_bus
        subnodes = [internal_bus]

        # Discharging
        if self.v2g:
            vehicle_to_grid = Converter(
                label=facade_label + "-v2g",
                inputs={internal_bus: Flow()},
                outputs={
                    self.electricity_bus: Flow(
                        nominal_value=self.max_charging_power,
                        max=self.availability,
                        # **self.output_parameters
                    )
                },
                # Includes storage charging efficiencies
                conversion_factors={self.electricity_bus: self.efficiency_charging},
                # TODO maybe add battery efficiency + charger efficiency
            )
            subnodes.append(vehicle_to_grid)

        # Charging
        grid_to_vehicle = Converter(
            label=facade_label + "-g2v",
            inputs={
                self.electricity_bus: Flow(
                    nominal_value=self.max_charging_power,
                    max=self.availability,
                    # **self.output_parameters
                )
            },
            outputs={internal_bus: Flow()},
            conversion_factors={self.electricity_bus: self.efficiency_charging},
            # TODO maybe add battery efficiency + charger efficiency
        )
        subnodes.append(grid_to_vehicle)

        # Drive consumption
        if self.transport_commodity_bus:
        # if True:
            transport_commodity = Converter(
                label=facade_label + "-consumption-converter",
                inputs={
                    internal_bus: Flow(
                        nominal_value=self.max_charging_power,
                        max=self.availability,
                        # **self.output_parameters
                    )
                },
                outputs={self.transport_commodity_bus: Flow()},
                conversion_factors={self.bus: self.efficiency_charging},
                # TODO maybe add battery efficiency + charger efficiency
            )
            subnodes.append(transport_commodity)

        else:
            driving_consumption = Sink(
                label=facade_label + "-consumption",
                inputs={
                    internal_bus: Flow(
                        nominal_value=self.drive_power,
                        fix=self.drive_consumption,
                    )
                },
            )
            subnodes.append(driving_consumption)

        # Storage inputs
        self.inputs.update(
            {
                internal_bus: Flow(
                    nominal_value=self.max_charging_power,
                    max=self.availability,
                    **self.input_parameters
                )
            }
        )
        # Storage output
        self.outputs.update(
            {
                internal_bus: Flow(
                    nominal_value=self.max_charging_power,
                    max=self.availability,
                )
            }
        )

        # many components in facade
        self.subnodes = subnodes
