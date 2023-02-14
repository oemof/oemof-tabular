from oemof.solph import Bus, Flow, Sink, Transformer, sequence
from oemof.solph.components import GenericStorage

from oemof.tabular._facade import Facade


class Bev(GenericStorage, Facade):
    r"""A fleet of Battery electric vehicles with vehicle-to-grid.

    Note that the investment option is not available for this facade at
    the current development state.

    Parameters
    ----------
    bus: oemof.solph.Bus
        An oemof bus instance where the storage unit is connected to.
    storage_capacity: numeric
        The total storage capacity of the vehicles (e.g. in MWh)
    capacity: numeric
        Total charging/discharging capacity of the vehicles.
    availability : array-like
        Ratio of available capacity for charging/vehicle-to-grid due to
        grid connection.
    drive_power : array-like
        Profile of the load of the fleet through driving relative amount.
    amount : numeric
        Total amount of energy consumed by driving. The drive_power profile
        will be scaled by this number.
    efficiency_charging: numeric
        Efficiency of charging the batteries, default: 1
    efficiency_discharging: numeric
        Efficiency of discharging the batteries, default: 1
    efficiency_v2g: numeric
        Efficiency of vehicle-to-grid, default: 1
    min_storage_level : array-like
        Profile of minimum storage level.
    max_storage_level : array-like
        Profile of maximum storage level.
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
    ...     name='my_bev',
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

    def __init__(self, *args, **kwargs):

        kwargs.update(
            {
                "_facade_requires_": [
                    "bus",
                    "carrier",
                    "tech",
                    "availability",
                    "drive_power",
                    "amount",
                ]
            }
        )
        super().__init__(*args, **kwargs)

        self.storage_capacity = kwargs.get("storage_capacity")

        self.capacity = kwargs.get("capacity")

        self.efficiency_charging = kwargs.get("efficiency_charging", 1)

        self.efficiency_discharging = kwargs.get("efficiency_discharging", 1)

        self.efficiency_v2g = kwargs.get("efficiency_v2g", 1)

        self.profile = kwargs.get("profile")

        self.marginal_cost = kwargs.get("marginal_cost", 0)

        self.input_parameters = kwargs.get("input_parameters", {})

        self.output_parameters = kwargs.get("output_parameters", {})

        self.expandable = bool(kwargs.get("expandable", False))

        self.build_solph_components()

    def build_solph_components(self):

        self.nominal_storage_capacity = self.storage_capacity

        self.inflow_conversion_factor = sequence(self.efficiency_charging)

        self.outflow_conversion_factor = sequence(self.efficiency_discharging)

        if self.expandable:
            raise NotImplementedError(
                "Investment for bev class is not implemented."
            )

        internal_bus = Bus(label=self.label + "-internal_bus")

        vehicle_to_grid = Transformer(
            carrier=self.carrier,
            tech=self.tech,
            label=self.label + "-vehicle_to_grid",
            inputs={internal_bus: Flow()},
            outputs={
                self.bus: Flow(
                    nominal_value=self.capacity,
                    max=self.availability,
                    variable_costs=self.marginal_cost,
                    **self.output_parameters
                )
            },
            conversion_factors={internal_bus: self.efficiency_v2g},
        )

        drive_power = Sink(
            label=self.label + "-drive_power",
            inputs={
                internal_bus: Flow(
                    nominal_value=self.amount,
                    actual_value=self.drive_power,
                    fixed=True,
                )
            },
        )

        self.inputs.update(
            {
                self.bus: Flow(
                    nominal_value=self.capacity,
                    max=self.availability,
                    **self.input_parameters
                )
            }
        )

        self.outputs.update({internal_bus: Flow()})

        self.subnodes = (internal_bus, drive_power, vehicle_to_grid)
