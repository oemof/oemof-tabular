import pkg_resources as pkg

from oemof.energy_system import EnergySystem as ES

from oemof.tabular.datapackage import deserialize_energy_system
from oemof.tabular.facades import TYPEMAP


def test_example_datapackage_readability():
    """ The example datapackages can be read and loaded.
    """

    systems = []
    for example in pkg.resource_listdir(
        'oemof.tabular', 'examples/datapackages'):

        systems.append(
            deserialize_energy_system(
                ES,
                pkg.resource_filename(
                    'oemof.tabular',
                    'examples/datapackages/{}/datapackage.json'.format(example)),
                typemap=TYPEMAP)
            )

    for system in systems:
        assert (type(system) is ES)
