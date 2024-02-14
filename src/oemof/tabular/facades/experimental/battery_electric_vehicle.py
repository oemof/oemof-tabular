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
        If `expandable` is set to True, this value represents the average charging
        power in kW. Otherwise, it denotes the charging power for the entire fleet in
        MW.
        todo: check units
    maximum_charging_power_investment: float or sequence
        Maximum charging power addition in investment optimization. Defined per period
        p for a multi-period model.
    availability : float, array of float
        Availability of the fleet at the charging stations (e.g. 0.8).
    storage_capacity: int
        If `expandable` is set to True, this value represents the average storage
        capacity in kWh. Otherwise, it denotes the charging power for the entire fleet
        in MWh.
        todo: check units
    min_storage_level : array of float
        This parameter is inherited from the :class:`GenericStorage` class.
        Relative profile of minimum storage level (min SOC).The normed minimum
        storage content as fraction of the storage capacity or the capacity
        that has been invested into (between 0 and 1).
    max_storage_level : array of float
        This parameter is inherited from the :class:`GenericStorage` class.
        Relative profile of maximum storage level (max SOC).
    drive_power: int
        The total driving capacity of the fleet (e.g. in MW) if no mobility_bus
        is connected.
    drive_consumption : array of float
        Relative profile of drive consumption of the fleet
    v2g: bool
        If True, Vehicle-to-grid option is enabled, default: False
    loss_rate: float
        This parameter is inherited from the :class:`GenericStorage` class.
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
    commodity_conversion_rate: float
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
        The rate of storage capacity invested per unit of charging power.
        For example, if invest_c_rate is 3, it indicates that 3 units of storage
        capacity are invested for every unit of charging/discharging power. If
        invest_c_rate is not provided, it is calculated based on the ratio of
        storage_capacity to charging_power. If invest_c_rate, storage_capacity, and
        charging_power are provided, invest_c_rate is validated against the calculated
        value and a warning is issued if they do not match.
    bev_invest_costs: float, array of float
        Investment costs for new vehicle unit. EUR/vehicle
    variable_costs: float, array of float
        Variable costs of the fleet (e.g. in EUR/MWh).
    fixed_costs: float, array of float
        Operation independent costs for existing and new vehicle units.
         (e.g. EUR/(vehicle*a))
    fixed_investment_costs: float, array of float
        todo: add description.
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


    Note
    ----
    As the Bev is a sub-class of `oemof.solph.GenericStorage` you also
    pass all arguments of this class.

    - Costs are determined by the charging converter (storage input converter) costs,
    assuming the size equality of storage input and output converters. Additionally,
    it guarantees that the V2G converter remains smaller than or equal to the storage
    output converter.
    - Access to investment variables is restricted until the component is added to the
    energy system.
    - Utilizes the constraint facade :class:`BevEqualInvest`.

    """

    electricity_bus: Bus = None

    commodity_bus: Bus = None

    charging_power: float = None

    maximum_charging_power_investment: Union[float, Sequence[float]] = None

    availability: Union[float, Sequence[float]] = 1

    storage_capacity: float = None

    drive_power: int = 0

    drive_consumption: Sequence[float] = None

    v2g: bool = False

    efficiency_mob_g2v: float = 1

    efficiency_mob_v2g: float = 1

    efficiency_sto_in: float = 1

    efficiency_sto_out: float = 1

    efficiency_mob_electrical: float = 1

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
                maximum=getattr(
                    self, "maximum_charging_power_investment", None
                ),
                lifetime=getattr(self, "lifetime", None),
                age=getattr(self, "age", 0),
                fixed_costs=0,
            )
            return investment
        else:
            return None

    def _invest_c_rate(self):
        """Determines the investment rate (invest_c_rate) based on the passed
        parameters:

        - If no parameters are passed, the default value of 1 is assigned.
        - If only invest_c_rate is passed, it is assigned directly.
        - If only storage_capacity and charging_power are passed, the invest_c_rate is
        calculated.
        - If invest_c_rate, storage_capacity, and charging_power are passed, it ensures
          that the calculated and passed invest_c_rate are equal. If not, the passed
          value is assigned and a warning is issued.
        """
        if (
            self.invest_c_rate is None
            and self.storage_capacity is None
            and self.cahrging_power is None
        ):
            self.invest_c_rate = 1
        elif (
            self.invest_c_rate is None
            and self.storage_capacity is not None
            and self.charging_power is not None
        ):
            self.invest_c_rate = self.storage_capacity / self.charging_power
        elif (
            self.invest_c_rate is not None
            and self.storage_capacity is not None
            and self.charging_power is not None
        ):
            calculated_invest_c_rate = (
                self.storage_capacity / self.charging_power
            )
            if calculated_invest_c_rate != self.invest_c_rate:
                print(
                    f"Warning: The passed invest_c_rate ({self.invest_c_rate}) does not"
                    f" match the calculated value ({calculated_invest_c_rate})."
                )
        else:
            self.invest_c_rate = 1
            print(
                f"Warning: invest_c_rate could not be calculated. Standard value of 1"
                f" was assigned."
            )

    def build_solph_components(self):
        # use label as prefix for subnodes
        self.facade_label = self.label
        self.label = self.label + "-storage"

        # convert to solph sequences
        self.availability = solph_sequence(self.availability)

        self.balanced = self.balanced  # TODO to be false in multi-period

        # create internal bus
        internal_bus = Bus(label=self.facade_label + "-bus")
        self.bus = internal_bus
        subnodes = [internal_bus]

        # Calculate invest_c_rate
        self._invest_c_rate()

        if self.expandable:
            self.investment = Investment(
                ep_costs=0,
                lifetime=getattr(self, "lifetime", None),
                age=getattr(self, "age", 0),
                fixed_costs=0,
            )
        else:
            self.nominal_storage_capacity = self.storage_capacity

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
            # contains the whole investment costs for bev
            flow_in = Flow(
                # max=self.availability,
                investment=Investment(
                    ep_costs=self.bev_invest_costs,
                    maximum=getattr(
                        self, "maximum_charging_power_investment", None
                    ),
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


# ToDo: update docstring
@dataclass_facade
class IndividualMobilitySector(Facade):
    r"""A fleet of Battery electric vehicles with different controlled/flexible
    charging (G2V), vehicle-to-grid (V2G) or uncontrolled/fixed charging (inflex).
    Note that the investment option is not available for this facade at
    the current development state. todo: still up to date?
    Parameters
    ----------

    label: str
        A string representing the label for the IndividualMobilitySector instance.
    electricity_bus: Bus
        An oemof bus instance representing the connection to the electricity grid.
    transport_commodity_bus: Bus
        An oemof bus instance representing the connection to the transport commodity.
    charging_power_flex: float
        The charging power for grid-to-vehicle (G2V) and vehicle-to-grid (V2G)
        operations. If `expandable` is set to True, this value represents the average
        charging power in kW. Otherwise, it denotes the charging power for the entire
        fleet in MW.
        todo: check units
    charging_power_inflex: float
        The charging power for uncontrolled/fixed charging (inflex) operations. If
        `expandable` is set to True, this value represents the average charging power
        in kW. Otherwise, it denotes the charging power for the entire fleet in MW.
        todo: check units
    maximum_charging_power_investment: float or sequence
        Maximum charging power addition in investment optimization. Defined per period
        p for a multi-period model.
    availability: Union[float, Sequence[float]]
        The ratio of available capacity for charging/vehicle-to-grid due to grid
        connection.
    storage_capacity_flex: float
        The storage capacity for grid-to-vehicle (G2V) and vehicle-to-grid (V2G)
        operations. If `expandable` is set to True, this value represents the average
        storage capacity in kWh. Otherwise, it denotes the charging power for the entire
        fleet in MWh.
        todo: check units
    storage_capacity_inflex: float
        The storage capacity for uncontrolled/fixed charging (inflex) operations. If
        `expandable` is set to True, this value represents the average storage capacity
        in kWh. Otherwise, it denotes the charging power for the entire fleet in MWh.
        todo: check units
    min_storage_level: Union[float, Sequence[float]]
        The profile of minimum storage level (min SOC).
    max_storage_level: Union[float, Sequence[float]]
        The profile of maximum storage level (max SOC).
    drive_power: int
        The total driving capacity of the fleet (e.g. in MW) if no mobility_bus
        is connected.
    drive_consumption: Sequence[float]
        The profile of drive consumption of the fleet (relative to drive_power).
    loss_rate: float
        The relative loss of the storage content per time unit (e.g. hour).
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
    commodity_conversion_rate: float
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
        The rate of storage capacity invested per unit of charging power.
        For example, if invest_c_rate is 3, it indicates that 3 units of storage
        capacity are invested for every unit of charging/discharging power. If
        invest_c_rate is not provided, it is calculated based on the ratio of
        storage_capacity to charging_power. If invest_c_rate, storage_capacity, and
        charging_power are provided, invest_c_rate is validated against the calculated
        value and a warning is issued if they do not match.
    bev_invest_costs: float, array of float
        Investment costs for new vehicle unit. EUR/vehicle
    fixed_costs: float, array of float
        Operation independent costs for existing and new vehicle units.
         (e.g. EUR/(vehicle*a))
    fixed_investment_costs: float, array of float
        todo: add description.
    variable_costs: float, array of float
        Variable costs of the fleet (e.g. in EUR/MWh).
    balanced : boolean
        Couple storage level of first and last time step.
        (Total inflow and total outflow are balanced.)
    input_parameters_inflex: dict
        Dictionary to specify parameters on the input edge for uncontrolled/fixed
        charging. You can use all keys that are available for the
        oemof.solph.network.Flow class. e.g. fixed charging timeseries for the storage
        can be passed with {"fix": [1,0.5,...]}
    output_parameters: dict
        Dictionary to specify parameters on the output edge. You can use
        all keys that are available for the  oemof.solph.network.Flow class. e.g. fixed
        discharging timeseries for the storage can be passed with {"fix": [1,0.5,...]}

    """

    # TODO: match data formats with actual data
    # Todo: wo müssen werte angegeben werden?

    label: str

    electricity_bus: Bus = None

    transport_commodity_bus: Bus = None

    charging_power_flex: float = None

    charging_power_inflex: float = None

    maximum_charging_power_investment: Union[float, Sequence[float]] = None

    availability: Union[float, Sequence[float]] = 1

    storage_capacity_flex: float = 0

    storage_capacity_inflex: float = 0

    min_storage_level: Union[float, Sequence[float]] = 0

    max_storage_level: Union[float, Sequence[float]] = 1

    drive_power: int = 0

    drive_consumption: Sequence[float] = None

    loss_rate: float = 0

    efficiency_mob_g2v: float = 1

    efficiency_mob_v2g: float = 1

    efficiency_sto_in: float = 1

    efficiency_sto_out: float = 1

    efficiency_mob_electrical: float = 1

    commodity_conversion_rate: float = 1

    expandable: bool = False

    lifetime: int = 20

    age: int = 0

    invest_c_rate: Sequence[float] = None

    bev_invest_costs: Sequence[float] = None

    fixed_costs: Union[float, Sequence[float]] = 0

    fixed_investment_costs: float = 0

    variable_costs: Union[float, Sequence[float]] = 0

    balanced: bool = False

    input_parameters_inflex: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    def build_solph_components(self):
        mobility_nodes = [self.transport_commodity_bus]

        bev_controlled_g2v = Bev(
            type="bev",
            label=self.label + "_G2V",
            electricity_bus=self.electricity_bus,
            commodity_bus=self.transport_commodity_bus,
            charging_power=self.charging_power_flex,
            maximum_charging_power_investment=self.maximum_charging_power_investment,
            availability=self.availability,
            storage_capacity=self.storage_capacity_flex,  # defined via constraint
            min_storage_level=self.min_storage_level,
            max_storage_level=self.max_storage_level,
            drive_consumption=self.drive_consumption,
            v2g=False,
            loss_rate=self.loss_rate,
            efficiency_mob_g2v=self.efficiency_mob_g2v,
            efficiency_mob_v2g=0,
            efficiency_sto_in=self.efficiency_sto_in,
            efficiency_sto_out=self.efficiency_sto_out,
            efficiency_mob_electrical=self.efficiency_mob_electrical,
            commodity_conversion_rate=self.commodity_conversion_rate,
            expandable=self.expandable,
            lifetime=self.lifetime,
            age=self.age,
            invest_c_rate=self.invest_c_rate,
            bev_invest_costs=self.bev_invest_costs,
            fixed_costs=self.fixed_costs,
            fixed_investment_costs=self.fixed_investment_costs,  # todo: added for test
            variable_costs=self.variable_costs,
            balanced=self.balanced,
        )

        mobility_nodes.append(bev_controlled_g2v)

        bev_controlled_v2g = Bev(
            type="bev",
            label=self.label + "_V2G",
            electricity_bus=self.electricity_bus,
            commodity_bus=self.transport_commodity_bus,
            charging_power=self.charging_power_flex,
            maximum_charging_power_investment=self.maximum_charging_power_investment,
            availability=self.availability,
            storage_capacity=self.storage_capacity_flex,
            min_storage_level=self.min_storage_level,
            max_storage_level=self.max_storage_level,
            drive_consumption=self.drive_consumption,
            v2g=True,
            loss_rate=self.loss_rate,
            efficiency_mob_g2v=self.efficiency_mob_g2v,
            efficiency_mob_v2g=self.efficiency_mob_v2g,
            efficiency_sto_in=self.efficiency_sto_in,
            efficiency_sto_out=self.efficiency_sto_out,
            efficiency_mob_electrical=self.efficiency_mob_electrical,
            commodity_conversion_rate=self.commodity_conversion_rate,
            expandable=self.expandable,
            lifetime=self.lifetime,
            age=self.age,
            invest_c_rate=self.invest_c_rate,
            bev_invest_costs=self.bev_invest_costs,
            fixed_costs=self.fixed_costs,
            fixed_investment_costs=self.fixed_investment_costs,  # todo: added for test
            variable_costs=self.variable_costs,
            balanced=self.balanced,
        )

        mobility_nodes.append(bev_controlled_v2g)

        bev_inflex = Bev(
            type="bev",
            label=self.label + "_Inflex",
            electricity_bus=self.electricity_bus,
            commodity_bus=self.transport_commodity_bus,
            charging_power=self.charging_power_inflex,
            maximum_charging_power_investment=self.maximum_charging_power_investment,
            availability=self.availability,
            storage_capacity=self.storage_capacity_inflex,
            min_storage_level=self.min_storage_level,
            max_storage_level=self.max_storage_level,
            drive_consumption=self.drive_consumption,
            v2g=False,
            loss_rate=self.loss_rate,
            efficiency_mob_g2v=self.efficiency_mob_g2v,
            efficiency_mob_v2g=0,
            efficiency_sto_in=self.efficiency_sto_in,
            efficiency_sto_out=self.efficiency_sto_out,
            efficiency_mob_electrical=self.efficiency_mob_electrical,
            commodity_conversion_rate=self.commodity_conversion_rate,
            expandable=self.expandable,
            lifetime=self.lifetime,
            age=self.age,
            invest_c_rate=self.invest_c_rate,
            bev_invest_costs=self.bev_invest_costs,
            fixed_costs=self.fixed_costs,
            fixed_investment_costs=self.fixed_investment_costs,  # todo: added for test
            variable_costs=self.variable_costs,
            balanced=self.balanced,
            input_parameters=self.input_parameters_inflex,
        )

        mobility_nodes.append(bev_inflex)

        # many components in facade
        self.subnodes = mobility_nodes
