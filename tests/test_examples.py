import pkg_resources as pkg

from oemof.energy_system import EnergySystem as ES

from oemof.tabular.facades import TYPEMAP


def test_example_datapackage_readability():
    """ The example datapackages can be read and loaded.
    """
    systems = [
            ES.from_datapackage(pkg.resource_filename(
                    'oemof.tabular',
                    'examples/datapackages/{}/datapackage.json'.format(example)
                ),
                typemap=TYPEMAP)
            for example in pkg.resource_listdir(
                'oemof.tabular',
                'examples/datapackages'
            )]
    for system in systems:
        assert (type(system) is ES)

