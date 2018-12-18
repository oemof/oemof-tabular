import pkg_resources as pkg

from oemof.energy_system import EnergySystem as ES

from oemof.tabular.facades import TYPEMAP
# The import below is only used to monkey patch `EnergySystem`.
# Hence the `noqa` because otherwise, style checkers would complain about an
# unused import.
import oemof.tabular.datapackage  # noqa: F401


def test_example_datapackage_readability():
    """ The example datapackages can be read and loaded.
    """

    systems = []
    for example in pkg.resource_listdir(
        'oemof.tabular', 'examples/datapackages'):

        systems.append(
            ES.from_datapackage(
                pkg.resource_filename(
                    'oemof.tabular',
                    'examples/datapackages/{}/datapackage.json'.format(example)),
                typemap=TYPEMAP)
            )

    for system in systems:
        assert (type(system) is ES)
