from dataclasses import field
from typing import Sequence, Union

from oemof.solph import Investment
from oemof.solph._plumbing import sequence as solph_sequence
from oemof.solph.buses import Bus
from oemof.solph.components import Converter, GenericStorage, Sink
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class Bev(GenericStorage, Facade):
    r"""A fleet of Battery electric vehicles with controlled/flexible charging,
     (G2V), vehicle-to-grid (V2G) or uncontrolled/fixed charging (inflex).

    This facade consists of mulitple oemof.solph components:

    - a GenericStorage as storage unit
    - a Bus as internal bus
    - a Sink to model the drive consumption (if no mobility bus is
        given)
    - a Converter to convert the energy to the electricity bus (optional V2G)
    - a Converter to convert the energy to e.g. pkm (optional if mobility bus
      is given)

    Charging and discharging capacity is assumed to be equal.
    Multiple fleets can be modelled and connected to a common bus
    (commodity_bus) to apply one demand for all modelled fleets.

    Parameters
    ----------
    electricity_bus: oemof.solph.Bus
        The electricity bus where the BEV is connected to.
    commodity_bus: oemof.solph.Bus
        A bus which is used to connect a common demand for multiple BEV
        instances (optional).
    charging_power : int
        The total charging/discharging power of the fleet (e.g. in MW).
    charging_potential: int
        Maximum charging potential in investment optimization.
    availability : float, array of float
        Availability of the fleet at the charging stations (e.g. 0.8).
    storage_capacity: int
        The total storage capacity of the fleet (e.g. in MWh).
    initial_storage_capacity: float
        The relative storage content in the timestep before the first
        time step of optimization (between 0 and 1).

        Note: When investment mode is used in a multi-period model,
        `initial_storage_level` is not supported.
        Storage output is forced to zero until the storage unit is invested in.
    min_storage_level : array of float
        Relative profile of minimum storage level (min SOC).The normed minimum
        storage content as fraction of the storage capacity or the capacity
        that has been invested into (between 0 and 1).
    max_storage_level : array of float
        Relative profile of maximum storage level (max SOC).
    drive_power: int
        The total driving capacity of the fleet (e.g. in MW) if no mobility_bus
        is connected.
    drive_consumption : array of float
        Relative profile of drive consumption of the fleet
    v2g: bool
        If True, Vehicle-to-grid option is enabled, default: False
    loss_rate: float
        The relative loss/self discharge of the storage content per time unit,
        default: 0
    efficiency_mob_g2v: float
        Efficiency at the charging station (grid-to-vehicle), default: 1
    efficiency_mob_v2g: float
        Efficiency at the charging station (vehicle-to-grid), default: 1
    efficiency_sto_in: float
        Efficiency of charging the batteries, default: 1
    efficiency_sto_out: float
        Efficiency of discharging the batteries, default: 1
    efficiency_mob_electrical: float
        Efficiency of the electrical drive train per 100 km (optional).
         default: 1
    pkm_conversion_rate: float
        Conversion rate from energy to e.g. pkm if mobility_bus passed
        (optional) default: 1
    expandable: bool
        If True, the fleet is expandable, default: False
        Charging_power and storage_capacity are then interpreted as existing
        capacities at the first investment period.
    lifetime: int
        Total lifetime of the fleet in years.
    age: int
        Age of the existing fleet at the first investment period in years.

    invest_c_rate: float
        Invested storage capacity per power rate
        (e.g. 60/20 = 3h charging/discharging time)
    bev_storage_capacity: int
        Storage capacity of one vehicle in kWh.
    bev_capacity: int
        Charging capacity of one vehicle in kW.

    bev_invest_costs: float, array of float
        Investment costs for new vehicle unit. EUR/vehicle
    fixed_costs: float, array of float
        Operation independent costs for existing and new vehicle units.
         (e.g. EUR/(vehicle*a))
    variable_costs: float, array of float
        Variable costs of the fleet (e.g. in EUR/MWh).
    fixed_investment_costs


    balanced : boolean
        Couple storage level of first and last time step.
        (Total inflow and total outflow are balanced.)

    input_parameters: dict
        Dictionary to specify parameters on the input edge. You can use
        all keys that are available for the  oemof.solph.network.Flow class.
        e.g. fixed charging timeseries for the storage can be passed with
        {"fix": [1,0.5,...]}
    output_parameters: dict
        see: input_parameters
        e.g. fixed discharging timeseries for the storage can be passed with
        {"fix": [1,0.5,...]}


    The vehicle fleet is modelled as a storage together with an internal
    sink with fixed flow:

    todo check formula
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
    # ...     loss_rate=0.01,
    ...     initial_storage_level=0,
    ...     min_storage_level=[0.1, 0.2, 0.15],
    ...     max_storage_level=[0.9, 0.95, 0.92],
    ...     efficiency=0.93
    ...     )

    """

    electricity_bus: Bus

    commodity_bus: Bus = None

    charging_power: float = 0

    minimum_charging_power: float = None

    charging_potential: float = None

    availability: Union[float, Sequence[float]] = 1

    storage_capacity: float = 0

    minimum_storage_capacity: float = 0

    storage_capacity_potential: float = None

    initial_storage_capacity: float = 0

    drive_power: int = 0

    drive_consumption: Sequence[float] = None

    v2g: bool = False

    efficiency_mob_g2v: float = 1

    efficiency_mob_v2g: float = 1

    efficiency_mob_electrical: float = 1

    efficiency_sto_in: float = 1

    efficiency_sto_out: float = 1

    commodity_conversion_rate: float = 1

    expandable: bool = False

    lifetime: int = 20

    age: int = 0

    invest_c_rate: Sequence[float] = None

    bev_invest_costs: Sequence[float] = None

    variable_costs: Union[float, Sequence[float]] = 0

    fixed_costs: Union[float, Sequence[float]] = 0

    fixed_investment_costs: Union[float, Sequence[float]] = 0

    balanced: bool = False

    input_parameters: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    def _converter_investment(self):
        """All parameters are passed, but no investment cost is considered.
        The investment cost will be considered by the storage inflow only.
        """
        if self.expandable:
            investment = Investment(
                ep_costs=0,
                maximum=self._get_maximum_additional_invest(
                    "charging_potential", "charging_power"
                ),
                minimum=getattr(self, "minimum_charging_power", 0),
                existing=getattr(self, "charging_power", 0),
                lifetime=getattr(self, "lifetime", None),
                age=getattr(self, "age", 0),
                fixed_costs=0,
            )
            return investment
        else:
            return None

    def build_solph_components(self):
        # use label as prefix for subnodes
        self.facade_label = self.label
        self.label = self.label + "-storage"

        # convert to solph sequences
        self.availability = solph_sequence(self.availability)

        # TODO: check if this is correct
        self.nominal_storage_capacity = self.storage_capacity
        # self.nominal_storage_capacity = self._nominal_value(
        #     self.storage_capacity)

        self.balanced = self.balanced  # TODO to be false in multi-period

        # create internal bus
        internal_bus = Bus(label=self.facade_label + "-bus")
        self.bus = internal_bus
        subnodes = [internal_bus]

        self.investment = Investment(
            ep_costs=0,
            maximum=self._get_maximum_additional_invest(
                "storage_capacity_potential", "storage_capacity"
            ),
            minimum=getattr(self, "minimum_storage_capacity", 0),
            existing=getattr(self, "storage_capacity", 0),
            lifetime=getattr(self, "lifetime", None),
            age=getattr(self, "age", 0),
            fixed_costs=0,
        )

        # ##### Vehicle2Grid Converter #####
        if self.v2g:
            vehicle_to_grid = Converter(
                label=self.facade_label + "-v2g",
                inputs={
                    internal_bus: Flow(
                        # variable_costs=self.carrier_cost,
                        # **self.input_parameters
                    )
                },
                outputs={
                    self.electricity_bus: Flow(
                        nominal_value=self._nominal_value(
                            value=self.charging_power
                        ),
                        # max=self.availability, # doesn't work with investment
                        variable_costs=None,
                        # investment=self._investment(bev=True),
                        investment=self._converter_investment(),
                    )
                },
                # Includes storage charging efficiencies
                conversion_factors={
                    self.electricity_bus: (self.efficiency_mob_v2g)
                },
            )
            subnodes.append(vehicle_to_grid)

        # Drive consumption
        if self.commodity_bus:
            # ##### Commodity Converter #####
            # converts energy to another commodity e.g. pkm
            # connects it to a special mobility bus
            commodity_converter = Converter(
                label=self.facade_label + "-2com",
                inputs={
                    internal_bus: Flow(
                        # **self.output_parameters
                    )
                },
                outputs={
                    self.commodity_bus: Flow(
                        nominal_value=self._nominal_value(self.charging_power),
                        # max=self.availability,
                        variable_costs=None,
                        # investment=self._investment(bev=True),
                        investment=self._converter_investment(),
                    )
                },
                conversion_factors={
                    self.commodity_bus: self.commodity_conversion_rate
                    * self.efficiency_mob_electrical
                    # * 100  # TODO pro 100 km?
                },
            )
            subnodes.append(commodity_converter)

        else:
            # ##### Consumption Sink #####
            # fixed demand for this fleet only
            if self.expandable:
                raise NotImplementedError(
                    "Consumption sink for expandable BEV not implemented yet!"
                    "Please use a `mobility_bus` + `Sink` instead. Optimizing"
                    "one fleet alone may not yield meaningful results."
                )
            else:
                driving_consumption = Sink(
                    label=self.facade_label + "-consumption",
                    inputs={
                        internal_bus: Flow(
                            nominal_value=self.drive_power,
                            fix=self.drive_consumption,
                        )
                    },
                )
            subnodes.append(driving_consumption)

        # ##### Storage ########
        if self.expandable:
            # self.capacity_cost = self.bev_invest_costs
            self.storage_capacity_cost = 0
            # self.investment = self._investment(bev=False)
            self.invest_relation_input_output = 1  # charge/discharge equal
            # invest_c_rate = Energy/Power = h
            self.invest_relation_input_capacity = (
                1 / self.invest_c_rate
            )  # Power/Energy
            self.invest_relation_output_capacity = (
                1 / self.invest_c_rate
            )  # Power/Energy

            for attr in ["invest_relation_input_output"]:
                if getattr(self, attr) is None:
                    raise AttributeError(
                        (
                            "You need to set attr " "`{}` " "for component {}"
                        ).format(attr, self.label)
                    )

            # ##### Grid2Vehicle #####
            # containts the whole investment costs for bev
            flow_in = Flow(
                # max=self.availability,
                investment=Investment(
                    ep_costs=self.bev_invest_costs,
                    maximum=self._get_maximum_additional_invest(
                        "charging_potential", "charging_power"
                    ),
                    existing=getattr(self, "charging_power", 0),
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                    fixed_costs=getattr(self, "fixed_investment_costs", None),
                ),
                variable_costs=self.variable_costs,
                **self.input_parameters,
            )
            # set investment, but no costs (as relation input / output = 1)
            flow_out = Flow(
                investment=Investment(
                    existing=getattr(self, "charging_power", 0),
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                ),
                **self.output_parameters,
            )
            # required for correct grouping in oemof.solph.components
            self._invest_group = True

        else:
            flow_in = Flow(
                nominal_value=self._nominal_value(self.charging_power),
                # max=self.availability,
                variable_costs=self.variable_costs,
                **self.input_parameters,
            )
            flow_out = Flow(
                nominal_value=self._nominal_value(self.charging_power),
                # max=self.availability,
                **self.output_parameters,
            )

        self.inflow_conversion_factor = solph_sequence(
            self.efficiency_mob_g2v * self.efficiency_sto_in
        )

        self.outflow_conversion_factor = solph_sequence(
            self.efficiency_sto_out
        )

        self.inputs.update({self.electricity_bus: flow_in})

        self.outputs.update({self.bus: flow_out})

        self._set_flows()

        # many components in facade
        self.subnodes = subnodes


# ToDo: remove facade-bus
# ToDo: name of class ok?
# ToDo: adjust parameters
# ToDo: adjust docstring
@dataclass_facade
class individual_mobility_sector(Facade):
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
    """

    electricity_bus: Bus

    storage_capacity: int

    drive_power: int

    max_charging_power: Union[float, Sequence[float]]

    availability: Sequence[float]

    label: str

    # type: str = "ind_mob_sec"

    drive_consumption: Sequence = None

    efficiency_charging: float = 1

    v2g: bool = False

    transport_commodity_bus: Bus = None

    input_parameters: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    expandable: bool = False

    def build_solph_components(self):
        transport_commodity_bus = Bus(label="transport_commodity")
        transport_commodity_bus.type = "bus"

        mobility_nodes = [transport_commodity_bus]

        bev_controlled_v2g = Bev(
            label="V2G",
            electricity_bus=self.electricity_bus,
            storage_capacity=self.storage_capacity,
            drive_power=self.drive_power,
            max_charging_power=self.max_charging_power,
            availability=self.availability,
            efficiency_charging=self.efficiency_charging,
            v2g=True,
            transport_commodity_bus=transport_commodity_bus,
        )

        mobility_nodes.append(bev_controlled_v2g)

        bev_controlled = Bev(
            label="BEV",
            electricity_bus=self.electricity_bus,
            storage_capacity=self.storage_capacity,
            drive_power=self.drive_power,
            max_charging_power=self.max_charging_power,
            availability=self.availability,
            efficiency_charging=self.efficiency_charging,
            v2g=False,
            transport_commodity_bus=transport_commodity_bus,
        )

        mobility_nodes.append(bev_controlled)

        pkm_demand = Load(
            label="pkm_demand",
            type="Load",
            carrier="pkm",
            bus=transport_commodity_bus,
            amount=400,
            profile=[0, 1, 0],
        )

        mobility_nodes.append(pkm_demand)

        # many components in facade
        self.subnodes = mobility_nodes
