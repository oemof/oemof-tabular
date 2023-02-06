from oemof.network.energy_system import EnergySystem
from oemof.solph import Model

from . import building  # noqa F401
from .reading import deserialize_constraints, deserialize_energy_system

EnergySystem.from_datapackage = classmethod(deserialize_energy_system)

Model.add_constraints_from_datapackage = deserialize_constraints
