from oemof.energy_system import EnergySystem

from .reading import deserialize_energy_system


EnergySystem.from_datapackage = classmethod(deserialize_energy_system)
