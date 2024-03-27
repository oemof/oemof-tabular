import logging
from collections.abc import Iterable
from dataclasses import field
from typing import Sequence, Union

from oemof.solph import Investment
from oemof.solph._plumbing import sequence as solph_sequence
from oemof.solph.buses import Bus
from oemof.solph.components import Converter, GenericStorage, Sink
from oemof.solph.flows import Flow

from oemof.tabular._facade import Facade, dataclass_facade


@dataclass_facade
class BevTech(GenericStorage, Facade):
    r"""A Battery electric vehicle technology with either controlled/flexible
    charging, (G2V), vehicle-to-grid (V2G) or uncontrolled/fixed charging
    (inflex).

    This facade consists of multiple oemof.solph components:

    - a GenericStorage as storage unit
    - a Bus as internal bus
    - a Sink to model the drive consumption (if no mobility bus is
        given)
    - a Converter to convert the energy to the electricity bus (optional V2G)
    - a Converter to convert the energy to e.g. pkm (optional if mobility bus
      is given)

    Charging and discharging capacity is assumed to be equal.
    Multiple bev technologies can be combined and connected to a common bus
    (commodity_bus) to apply one demand for all modelled bev techs. Use
    :class:`BevFleet` class for this

    Parameters
    ----------
    electricity_bus: oemof.solph.Bus
        The electricity bus where the BEV is connected to.
    demand_bus: oemof.solph.Bus
        A bus which is used to connect a common demand for multiple BEV
        instances (optional).
    charging_power : int
        If `expandable` is set to True, this value represents the average
        charging power in kW. Otherwise, it denotes the charging power for the
        entire fleet in MW.
        todo: check units
    maximum_charging_power_investment: float or sequence
        Maximum charging power addition in investment optimization. Defined per
         period p for a multi-period model.
    availability : float, array of float
        Availability of the fleet at the charging stations (e.g. 0.8).
    storage_capacity: int
        If `expandable` is set to True, this value represents the average
        storage capacity in kWh. Otherwise, it denotes the charging power for
        the entire fleet in MWh.
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
    efficiency_mob_g2v: float, array of float
        Efficiency at the charging station (grid-to-vehicle), default: 1
    efficiency_mob_v2g: float, array of float
        Efficiency at the charging station (vehicle-to-grid), default: 1
    efficiency_sto_in: float, array of float
        Efficiency of charging the batteries, default: 1
    efficiency_sto_out: float, array of float
        Efficiency of discharging the batteries, default: 1
    commodity_conversion_rate: float, array of float
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
        For example, invest_c_rate = 3 indicates that 3 units of storage
        capacity are invested for every unit of charging/discharging power. If
        invest_c_rate is not provided, it is calculated based on the ratio of
        storage_capacity to charging_power. If invest_c_rate, storage_capacity,
        and charging_power are provided, invest_c_rate is validated against the
        calculated value and a warning is issued if they do not match.
        Note: This rate is fixed over all periods.
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

    - Costs are determined by the charging converter (storage input converter)
    costs, assuming the size equality of storage input and output converters.
    Additionally, it guarantees that the V2G converter remains smaller than or
    equal to the storage output converter.
    - Access to investment variables is restricted until the component is added
    to the energy system.
    - Utilizes the constraint facade :class:`BevEqualInvest`.

    """

    label: str = None

    electricity_bus: Bus = None

    demand_bus: Bus = None

    charging_power: float = None

    maximum_charging_power_investment: Union[float, Sequence[float]] = None

    availability: Union[float, Sequence[float]] = 1

    storage_capacity: float = None

    drive_power: int = 0

    drive_consumption: Sequence[float] = None

    v2g: bool = False

    efficiency_mob_g2v: Union[float, Sequence[float]] = 1

    efficiency_mob_v2g: Union[float, Sequence[float]] = 1

    efficiency_sto_in: Union[float, Sequence[float]] = 1

    efficiency_sto_out: Union[float, Sequence[float]] = 1

    commodity_conversion_rate: Union[float, Sequence[float]] = 1

    expandable: bool = False

    lifetime: int = 20

    age: int = 0

    invest_c_rate: float = None

    bev_invest_costs: Sequence[float] = None

    variable_costs: Union[float, Sequence[float]] = 0

    fixed_costs: Union[float, Sequence[float]] = 0

    fixed_investment_costs: Union[float, Sequence[float]] = 0

    balanced: bool = False

    input_parameters: dict = field(default_factory=dict)

    output_parameters: dict = field(default_factory=dict)

    def _converter_investment(self, limit=False):
        """All parameters are passed, but no investment cost is considered.
        The investment cost will be considered by the storage inflow only.
        """
        if self.expandable:
            if limit:
                investment = Investment(
                    ep_costs=0,
                    maximum=getattr(
                        self, "maximum_charging_power_investment", None
                    ),
                    minimum=getattr(
                        self, "minimum_charging_power_investment", None
                    ),
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                    fixed_costs=0,
                )
            else:
                # no investment limitation e.g. drive power strain
                # only charging is limited by charger but not drive power
                investment = Investment(
                    ep_costs=0,
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
        - If only storage_capacity and charging_power are passed, the
            invest_c_rate is calculated.
        - If invest_c_rate, storage_capacity and charging_power are passed, it
            ensures that the calculated and passed invest_c_rate are equal. If
            not, the passed value is assigned and a warning is issued.
        """
        if (
            self.invest_c_rate is None
            and self.storage_capacity is None
            and self.charging_power is None
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
                logging.warning(
                    f"Warning: The passed invest_c_rate ({self.invest_c_rate})"
                    " does not match the calculated value "
                    f"({calculated_invest_c_rate})."
                )
        else:
            self.invest_c_rate = 1
            logging.warning(
                "Warning: invest_c_rate could not be calculated. Standard "
                "value of 1 was assigned."
            )

    @staticmethod
    def multiply_scalar_or_iterable(a, b):
        """Multiply scalars or each value of list"""
        if all([isinstance(i, Iterable) for i in [a, b]]):
            results = [x * y for x, y in zip(a, b)]
        elif all([isinstance(i, float) for i in [a, b]]):
            results = a * b
        else:
            raise ValueError(
                "Value of 'a' and 'b' must be iterables of"
                "float, or scalar float."
            )
        return results

    def build_solph_components(self):
        self.type = "bev"

        # use label as prefix for subnodes
        self.facade_label = self.label

        # Label of storage
        self.label = self.label + "-storage"

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
                        # nominal_value=self._nominal_value(
                        #     value=self.charging_power
                        # ),
                        # max=solph_sequence(self.availability),
                        # variable_costs=None,
                        # # investment=self._investment(bev=True),
                        # investment=self._converter_investment(limit=True),
                    )
                },
                outputs={
                    self.electricity_bus: Flow(
                        nominal_value=self._nominal_value(
                            value=self.charging_power
                        ),
                        max=solph_sequence(self.availability),
                        variable_costs=None,
                        # investment=self._investment(bev=True),
                        investment=self._converter_investment(limit=True),
                    )
                },
                # Includes storage charging efficiencies
                conversion_factors={
                    self.electricity_bus: solph_sequence(
                        self.efficiency_mob_v2g
                    )
                },
            )
            subnodes.append(vehicle_to_grid)

        # Drive consumption
        if self.demand_bus:
            # ##### Commodity Converter #####
            # converts energy to another commodity e.g. pkm
            # connects it to a special mobility bus
            commodity_converter = Converter(
                label=self.facade_label + "-conversion",
                inputs={
                    internal_bus: Flow(
                        # **self.output_parameters
                    )
                },
                outputs={
                    self.demand_bus: Flow(
                        nominal_value=self._nominal_value(self.charging_power),
                        variable_costs=None,
                        # no limitations for drive strain/power
                        investment=self._converter_investment(limit=False),
                    )
                },
                conversion_factors={
                    self.demand_bus: solph_sequence(
                        self.commodity_conversion_rate
                    )
                    # * 1/self.efficiency_mob_electrical
                    # * 100  # TODO pro 100 km?
                },
            )
            subnodes.append(commodity_converter)

        else:
            logging.warning(
                "BEV without demand-bus is not tested yet." "Take caution!"
            )
            # ##### Consumption Sink #####
            # fixed demand for this bev tech only
            if self.expandable:
                raise NotImplementedError(
                    "Consumption sink for expandable BEV not implemented yet!"
                    "Please use a `mobility_bus` + `Sink` instead. Optimizing"
                    "one bev-tech alone may not yield meaningful results."
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
            self.invest_relation_input_capacity = 1 / getattr(
                self, "invest_c_rate", 1
            )  # Power/Energy
            self.invest_relation_output_capacity = 1 / getattr(
                self, "invest_c_rate", 1
            )  # Power/Energy

            # ##### Grid2Vehicle #####
            # contains the whole investment costs for bev
            flow_in = Flow(
                # max=self.availability,
                investment=Investment(
                    ep_costs=self.bev_invest_costs,
                    maximum=getattr(
                        self, "maximum_charging_power_investment", None
                    ),
                    minimum=getattr(
                        self, "minimum_charging_power_investment", None
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
            # Trigger GenericInvestmentStorageBlock
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
            self.multiply_scalar_or_iterable(
                a=self.efficiency_mob_g2v, b=self.efficiency_sto_in
            )
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
class BevFleet(Facade):
    r"""A fleet of Battery electric vehicles of different :class:`BevTech`
    facades with controlled/flexible charging (G2V), vehicle-to-grid (V2G)
    and uncontrolled/fixed charging (inflex).

    Parameters
    ----------

    label: str
        A string representing the label for the IndividualMobilitySector
        instance.
    electricity_bus: Bus
        An oemof bus instance representing the connection to the electricity
        grid.
    demand_bus: Bus
        An oemof bus instance representing a common demand for the multiple BEV
        technologies.
    charging_power_flex: float
        The charging power for grid-to-vehicle (G2V) and vehicle-to-grid (V2G)
        operations. If `expandable` is set to True, this value represents the
        average charging power in kW. Otherwise, it denotes the charging power
        for the entire fleet in MW.
        todo: check units
    charging_power_inflex: float
        The charging power for uncontrolled/fixed charging (inflex) operations.
         If `expandable` is set to True, this value represents the average
         charging power in kW. Otherwise, it denotes the charging power for the
         entire fleet in MW.
        todo: check units
    minimum_charging_power_investment: float or sequence
        Minimum charging power addition in investment optimization. Defined per
        period p for a multi-period model.
    maximum_charging_power_investment: float or sequence
        Maximum charging power addition in investment optimization. Defined per
        period p for a multi-period model.
    availability_flex: Union[float, Sequence[float]]
        The ratio of available capacity for charging/vehicle-to-grid due to
        grid connection. todo: für flex/inflex
    availability_inflex: Union[float, Sequence[float]]
        Time series of fixed connection capacity.
    storage_capacity: float
        This value represents the average storage capacity in kWh if expandable
        is true. Otherwise it denotes the storage capacity for the entire fleet
         in MWh.
        todo: check units
    min_storage_level: Union[float, Sequence[float]]
        The profile of minimum storage level (min SOC).
    max_storage_level: Union[float, Sequence[float]]
        The profile of maximum storage level (max SOC).
    drive_power: int
        The total driving capacity of the fleet (e.g. in MW) if no mobility_bus
        is connected.
    drive_consumption: Sequence[float]
        The drive consumption profil of the fleet (relative to drive_power).
    loss_rate: float
        The relative loss of the storage content per time unit (e.g. hour).
    efficiency_mob_g2v: float, array of float
        Efficiency at the charging station (grid-to-vehicle), default: 1
    efficiency_mob_v2g: float, array of float
        Efficiency at the charging station (vehicle-to-grid), default: 1
    efficiency_sto_in: float, array of float
        Efficiency of charging the batteries, default: 1
    efficiency_sto_out: float, array of float
        Efficiency of discharging the batteries, default: 1
    commodity_conversion_rate: float, array of float
        Conversion rate from energy to e.g. pkm if demand_bus is passed
        (optional). Could also just be eletrical_drive_efficiency. default: 1
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
        For example, if invest_c_rate is 3, it indicates that 3 units of
        storage capacity are invested for every unit of charging/discharging
        power. If invest_c_rate is not provided, it is calculated based on the
        ratio of storage_capacity to charging_power. If invest_c_rate,
        storage_capacity, and charging_power are provided, invest_c_rate is
        validated against the calculated value and a warning is issued if they
        do not match.
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
        Dictionary to specify parameters on the input edge for
        uncontrolled/fixed charging. You can use all keys that are available
        for the oemof.solph.network.Flow class. e.g. fixed charging timeseries
        for the storage can be passed with {"fix": [1,0.5,...]}
    output_parameters: dict
        Dictionary to specify parameters on the output edge. You can use
        all keys that are available for the  oemof.solph.network.Flow class
        e.g. fixed discharging timeseries for the storage can be passed
        with {"fix": [1,0.5,...]}

    """

    # TODO: match data formats with actual data
    # Todo: wo müssen werte angegeben werden?

    label: str = None

    electricity_bus: Bus = None

    demand_bus: Bus = None

    charging_power_flex: float = None

    charging_power_inflex: float = None

    minimum_charging_power_investment: Union[float, Sequence[float]] = None

    maximum_charging_power_investment: Union[float, Sequence[float]] = None

    availability_flex: Union[float, Sequence[float]] = 1

    availability_inflex: Union[float, Sequence[float]] = 1

    storage_capacity: float = 0

    min_storage_level: Union[float, Sequence[float]] = 0

    max_storage_level: Union[float, Sequence[float]] = 1

    drive_power: int = 0

    drive_consumption: Sequence[float] = None

    loss_rate: float = 0

    efficiency_mob_g2v: Union[float, Sequence[float]] = 1

    efficiency_mob_v2g: Union[float, Sequence[float]] = 1

    efficiency_sto_in: Union[float, Sequence[float]] = 1

    efficiency_sto_out: Union[float, Sequence[float]] = 1

    commodity_conversion_rate: Union[float, Sequence[float]] = 1  #

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

    def _demand_bus(self, bus):
        if self.demand_bus:
            return bus

    def build_solph_components(self):
        subnodes = []

        # BEV Fleet Node connected to eletricity bus, bidirectional
        self.inputs.update({self.electricity_bus: Flow()})
        self.outputs.update({self.electricity_bus: Flow()})

        # BEV Fleet connector
        # merges BEV techs flows and is connected to demand bus
        if self.demand_bus:
            fleet = Bus(label=self.label + "-total")
            fleet.outputs.update({self.demand_bus: Flow()})
            subnodes.append(fleet)

        # BEV controlled flexibility
        bev_controlled_g2v = BevTech(
            label=self.label + "_G2V",
            electricity_bus=self,
            demand_bus=self._demand_bus(fleet),
            charging_power=self.charging_power_flex,
            maximum_charging_power_investment=self.maximum_charging_power_investment,  # noqa
            availability=self.availability_flex,
            storage_capacity=self.storage_capacity,
            min_storage_level=self.min_storage_level,
            max_storage_level=self.max_storage_level,
            drive_consumption=self.drive_consumption,
            v2g=False,
            loss_rate=self.loss_rate,
            efficiency_mob_g2v=self.efficiency_mob_g2v,
            efficiency_sto_in=self.efficiency_sto_in,
            efficiency_sto_out=self.efficiency_sto_out,
            commodity_conversion_rate=self.commodity_conversion_rate,
            expandable=self.expandable,
            lifetime=self.lifetime,
            age=self.age,
            invest_c_rate=self.invest_c_rate,
            bev_invest_costs=self.bev_invest_costs,
            fixed_costs=self.fixed_costs,
            fixed_investment_costs=self.fixed_investment_costs,  # todo: added for test # noqa
            variable_costs=self.variable_costs,
            balanced=self.balanced,
        )
        subnodes.append(bev_controlled_g2v)

        # BEV controlled flexibility with vehicle to grid
        bev_controlled_v2g = BevTech(
            label=self.label + "_V2G",
            electricity_bus=self,
            demand_bus=self._demand_bus(fleet),
            charging_power=self.charging_power_flex,
            maximum_charging_power_investment=self.maximum_charging_power_investment,  # noqa
            availability=self.availability_flex,
            storage_capacity=self.storage_capacity,
            min_storage_level=self.min_storage_level,
            max_storage_level=self.max_storage_level,
            drive_consumption=self.drive_consumption,
            v2g=True,
            loss_rate=self.loss_rate,
            efficiency_mob_g2v=self.efficiency_mob_g2v,
            efficiency_mob_v2g=self.efficiency_mob_v2g,
            efficiency_sto_in=self.efficiency_sto_in,
            efficiency_sto_out=self.efficiency_sto_out,
            commodity_conversion_rate=self.commodity_conversion_rate,
            expandable=self.expandable,
            lifetime=self.lifetime,
            age=self.age,
            invest_c_rate=self.invest_c_rate,
            bev_invest_costs=self.bev_invest_costs,
            fixed_costs=self.fixed_costs,
            fixed_investment_costs=self.fixed_investment_costs,  # todo: added for test # noqa
            variable_costs=self.variable_costs,
            balanced=self.balanced,
        )
        subnodes.append(bev_controlled_v2g)

        # BEV uncontrolled with no flexibility but storage buffer
        bev_inflex = BevTech(
            label=self.label + "_inflex",
            electricity_bus=self,
            demand_bus=self._demand_bus(fleet),
            charging_power=self.charging_power_inflex,
            maximum_charging_power_investment=self.maximum_charging_power_investment,  # noqa
            availability=self.availability_inflex,
            storage_capacity=self.storage_capacity,
            min_storage_level=self.min_storage_level,
            max_storage_level=self.max_storage_level,
            drive_consumption=self.drive_consumption,
            v2g=False,
            loss_rate=self.loss_rate,
            efficiency_mob_g2v=self.efficiency_mob_g2v,
            efficiency_mob_v2g=0,
            efficiency_sto_in=self.efficiency_sto_in,
            efficiency_sto_out=self.efficiency_sto_out,
            commodity_conversion_rate=self.commodity_conversion_rate,
            expandable=self.expandable,
            lifetime=self.lifetime,
            age=self.age,
            invest_c_rate=self.invest_c_rate,
            bev_invest_costs=self.bev_invest_costs,
            fixed_costs=self.fixed_costs,
            fixed_investment_costs=self.fixed_investment_costs,  # todo: added for test # noqa
            variable_costs=self.variable_costs,
            balanced=self.balanced,
            input_parameters=self.input_parameters_inflex,
        )
        subnodes.append(bev_inflex)

        # Add subnodes to facade
        self.subnodes = subnodes
