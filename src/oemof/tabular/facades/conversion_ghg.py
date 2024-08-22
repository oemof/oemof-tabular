import dataclasses

from oemof.solph._plumbing import sequence
from oemof.solph.flows import Flow

from oemof import solph

from .conversion import Conversion


@dataclasses.dataclass(unsafe_hash=False, frozen=False, eq=False)
class ConversionGHG(Conversion):
    r"""
    Conversion unit with one input, one output and  green house gas outputs.

    Cost parameters like `carrier_cost` are associated with `from_bus` like in
    Conversion facade.
    The emission factors are also associated to `from_bus`


    Parameters
    ----------
    from_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its input.
    to_bus: oemof.solph.Bus
        An oemof bus instance where the conversion unit is connected to with
        its output.
    capacity: numeric
        The conversion capacity (output side) of the unit.
    efficiency: numeric
        Efficiency of the conversion unit (0 <= efficiency <= 1). Default: 1
    marginal_cost: numeric
        Marginal cost for one unit of produced output. Default: 0
    carrier_cost: numeric
        Carrier cost for one unit of used input. Default: 0
    capacity_cost: numeric
        Investment costs per unit of output capacity.
        If capacity is not set, this value will be used for optimizing the
        conversion output capacity.
    expandable: boolean or numeric (binary)
        True, if capacity can be expanded within optimization. Default: False.
    capacity_potential: numeric
        Maximum invest capacity in unit of output capacity.
    capacity_minimum: numeric
        Minimum invest capacity in unit of output capacity.
    input_parameters: dict (optional)
        Set parameters on the input edge of the conversion unit
        (see oemof.solph for more information on possible parameters)
    ouput_parameters: dict (optional)
        Set parameters on the output edge of the conversion unit
         (see oemof.solph for more information on possible parameters)

    Notes
    -----
    Emission buses carring the green house gases (GHG) are defined by starting
    with 'emission_bus', see Examples section.
    Emission factors are defined by the following naming convention:
    'emission_factor_<label_of_emission_bus>.

    Examples
    ---------
    Defining a ConversionGHG:

    >>> from oemof import solph

    >>> bus_biomass = solph.Bus("biomass")
    >>> bus_heat = solph.Bus("heat")
    >>> bus_co2 = solph.Bus("co2")

    >>> bus_biomass.type, bus_heat.type, bus_co2.type = "bus", "bus", "bus"

    >>> conversion = ConversionGHG(
    ...    label="biomass_plant",
    ...    carrier="biomass",
    ...    tech="st",
    ...    from_bus=bus_biomass,
    ...    to_bus=bus_heat,
    ...    emission_bus_0=bus_co2,
    ...    capacity=100,
    ...    efficiency=0.4,
    ...    emission_factor_co2=56)
    >>> conversion.conversion_factors[bus_co2].default
    56
    """

    def __init__(self, **kwargs):
        super().__init__(
            **kwargs,
        )

        buses = {
            key: value
            for key, value in kwargs.items()
            if type(value) is type(solph.Bus())
        }

        self.build_solph_components()  # inputs, outputs, conversion_factors
        self.init_emission_buses(kwargs)
        self.init_emission_factors(buses, kwargs)

    def init_emission_buses(self, kwargs):
        """Adds emissions buses as output flows and drops them from kwargs"""
        for key, value in list(kwargs.items()):
            if key.startswith("emission_bus"):
                # then value is a solph.Bus object and is added to self.outputs
                self.outputs.update({value: Flow()})
                kwargs.pop(key)

    def init_emission_factors(self, buses, kwargs):
        """Adds emission factors as `conversion_factors"""
        for key, value in list(kwargs.items()):
            if key.startswith("emission_factor"):
                bus_label = key.split("_")[-1]
                try:
                    bus = [
                        bus
                        for bus in buses.items()
                        if bus[1].label == bus_label
                    ][0][1]
                except IndexError:
                    raise Warning(
                        f"Emission factor is given for a non-existent emission"
                        f" bus: '{bus_label}'. Check your inputs for "
                        f"'{self.label}' of type '{self.type}'. "
                    )
                self.conversion_factors.update({bus: sequence(value)})
                kwargs.pop(key)

        # check that every bus has a conversion factor, otherwise an error
        # occurs in oemof.solph.components._converter.py
        if not len(self.outputs) + len(self.inputs) == len(
            self.conversion_factors
        ):
            raise Warning(
                f"Every emission_bus needs an emission_factor. Check your "
                f"inputs for '{self.label}' of type '{self.type}'."
            )
