from oemof.network.energy_system import EnergySystem

from . import building
from .reading import deserialize_energy_system

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)
