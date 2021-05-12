from oemof.network.energy_system import EnergySystem

from .reading import deserialize_energy_system
from . import processing, building, aggregation

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)
