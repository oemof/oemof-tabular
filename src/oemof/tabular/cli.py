"""
Module that contains the command line app.

"""
import click
from datapackage import Package, exceptions
import pandas as pd


def _test(ctx, package):
    """
    """
    p = Package(package)
    for r in p.resources:
        try:
            r.read(keyed=True)
            fks = r.descriptor['schema'].get('foreignKeys', [])
            for fk in fks:
                if fk.get('fields') == 'profile':
                    profile = p.get_resource(fk['reference']['resource'])
                    field_names = set([
                        field['name']
                        for field in profile.descriptor['schema']['fields']
                    ])
                    field_names.remove('timeindex')
                    profile_names = set(
                        pd.DataFrame(r.read(keyed=True))['profile'])

                    diff = field_names.symmetric_difference(profile_names)
                    if len(diff) > 0:
                        for d in diff:
                            print(
                                ("Foreign key error for {} in "
                                 " resource {} and {}.".format(d, r.name,
                                                               profile.name))
                            )

        except:
            raise exceptions.DataPackageException(
                (
                    "Could not read resource {} from datpackage "
                    "with name {}".format(r.name, p.descriptor['name'])
                 )
            )
    print("Successfully tested datapackage {}.".format(
            p.descriptor['name']))


@click.group(chain=True)

@click.pass_context
def cli(ctx, **kwargs):
    ctx.obj = kwargs

@cli.command()
@click.argument("package", type=str, default="datapackage.json")
@click.pass_context
def test(ctx, package):
    _test(ctx, package)

def main():
    cli(obj={})
