from oemof.solph import Bus
from oemof.solph.buses.experimental import ElectricalBus
from oemof.solph.flows.experimental import ElectricalLine

from .backpressure_turbine import BackpressureTurbine
from .commodity import Commodity
from .conversion import Conversion
from .dispatchable import Dispatchable
from .excess import Excess
from .experimental.battery_electric_vehicle import BevFleet, BevTech
from .extraction_turbine import ExtractionTurbine
from .generator import Generator
from .heatpump import HeatPump
from .link import Link
from .load import Load
from .reservoir import Reservoir
from .shortage import Shortage
from .storage import Storage
from .volatile import Volatile

TYPEMAP = {
    "backpressure": BackpressureTurbine,
    "bus": Bus,
    "heatpump": HeatPump,
    "commodity": Commodity,
    "conversion": Conversion,
    "dispatchable": Dispatchable,
    "electrical bus": ElectricalBus,
    "electrical line": ElectricalLine,
    "excess": Excess,
    "extraction": ExtractionTurbine,
    "generator": Generator,
    "link": Link,
    "load": Load,
    "reservoir": Reservoir,
    "shortage": Shortage,
    "storage": Storage,
    "volatile": Volatile,
    "bev tech": BevTech,
    "bev fleet": BevFleet,
}

TECH_COLOR_MAP = {
    "acaes": "brown",
    "ocgt": "gray",
    "st": "darkgray",
    "ccgt": "lightgray",
    "heat-storage": "lightsalmon",
    "extraction-turbine": "orange",
    "heat-pump": "skyblue",
    "motoric-chp": "gray",
    "electro-boiler": "darkblue",
    "pv": "gold",
    "onshore": "skyblue",
    "offshore": "darkblue",
    "ce": "olivedrab",
    "hp": "lightsalmon",
    "battery": "lightsalmon",
    "ror": "aqua",
    "phs": "darkblue",
    "reservoir": "slateblue",
    "biomass": "olivedrab",
    "storage": "lightsalmon",
    "battery": "lightsalmon",
    "import": "crimson",
}

CARRIER_COLER_MAP = {
    "biomass": "olivedrab",
    "lithium": "lightsalmon",
    "electricity": "darkred",
    "hydro": "aqua",
    "hydrogen": "magenta",
    "uranium": "yellow",
    "wind": "skyblue",
    "solar": "gold",
    "gas": "lightgray",
    "lignite": "chocolate",
    "coal": "darkgray",
    "waste": "yellowgreen",
    "oil": "black",
}
