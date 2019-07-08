from oemof.network import Bus
from oemof.energy_system import EnergySystem
import oemof

from oemof.tabular.facades import Reservoir
import oemof.tabular


def test_version_specification():
    """ `oemof.tabular`'s version specification is importable and a string.
    """
    assert isinstance(oemof.tabular.__version__, str)
    assert isinstance(oemof.__version__, str)


def test_project_name():
    """ `oemof.tabular`'s project name is importable and correct.
    """
    assert (oemof.tabular.__project__ == 'oemof.tabular')


def test_adding_subnodes():
    """ `Facade` subclasses correctly `connect` to and handle `add`.
    """
    es = EnergySystem()
    reservoir = Reservoir(
        label="r",
        bus=Bus("bus"),
        storage_capacity=1000,
        capacity=50,
        inflow=[1, 2, 6],
        loss_rate=0.01,
        initial_storage_level=0,
        max_storage_level=0.9,
        efficiency=0.93,
        carrier="carrier",
        tech="tech",
        profile="profile",
    )
    for sn in reservoir.subnodes:
        assert sn.label not in es.groups
    es.add(reservoir)
    for sn in reservoir.subnodes:
        assert sn.label in es.groups
