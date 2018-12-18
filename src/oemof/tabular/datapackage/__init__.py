from oemof.energy_system import EnergySystem

from .reading import deserialize_energy_system

from oemof.tabular.datapackage import building, processing, aggregation

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)
