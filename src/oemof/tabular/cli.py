"""
Module that contains the command line app.

"""
import collections
import copy

from datapackage import Package, exceptions

try:
    import click
except ImportError:
    raise ImportError("Need to install click to use cli!")

import pandas as pd

from .datapackage import building


def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d


scenarios = {}


# TODO: This definitely needs docstrings.
class Scenario(dict):
    @classmethod
    def from_path(cls, path):
        scenarios[path] = cls(
            building.read_build_config(path)
        )
        if "name" in scenarios[path]:
            name = scenarios[path]["name"]
            scenarios[name] = scenarios[path]
        return scenarios[path]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "parents" in self:
            for parent in self["parents"]:
                if parent in scenarios:
                    scenario = copy.deepcopy(scenarios[parent])
                else:
                    scenario = copy.deepcopy(type(self).from_path(parent))

                # hackish, but necessary to get self (the child) right
                # with all key/values of the parent and
                # it's own key/value pairs
                update(scenario, self)
                update(self, scenario)


def _test(ctx, package):
    """
    """
    p = Package(package)
    for r in p.resources:
        try:
            r.read(keyed=True)
            fks = r.descriptor["schema"].get("foreignKeys", [])
            for fk in fks:
                if fk.get("fields") == "profile":
                    profile = p.get_resource(fk["reference"]["resource"])
                    field_names = set(
                        [
                            field["name"]
                            for field in profile.descriptor["schema"]["fields"]
                        ]
                    )
                    field_names.remove("timeindex")
                    profile_names = set(
                        pd.DataFrame(r.read(keyed=True))["profile"]
                    )

                    diff = field_names.symmetric_difference(profile_names)
                    if len(diff) > 0:
                        for d in diff:
                            # TODO: Fix this.
                            #
                            # This will probably trigger an error. I vaguely
                            # remember that automatic concatenation of string
                            # literals only works if nothing is applied to
                            # them. Also, the format function doesn't cover the
                            # first interpolation.
                            # So heres what has to be done:
                            #   * write a test that triggers this `print`
                            #     statement (and therefore the error),
                            #   * move the `.format` call outside of the first
                            #     group of parenthesis, which fixes both
                            #     errors and
                            #   * use the test to check that the printed error
                            #     message looks correct.
                            print(
                                (
                                    "Foreign key error for {} in "
                                    " resource {} and {}.".format(
                                        d, r.name, profile.name
                                    )
                                )
                            )

        except Exception:
            # TODO: Fix this.
            # Again, this contains the same errors as above.
            # Also: when re-raising an exception, don't cover up the original
            # exception type and message.
            # See 715fa6aeecb45837c5679657a3a094d151862820 and its parent for
            # an IMHO better way of dealing with this.
            # So again:
            #   * fix how the Exception is raised,
            #   * write a test to trigger this line,
            #   * fix the generated message and
            #   * use the test to check the the exception's type and message.
            raise exceptions.DataPackageException(
                (
                    "Could not read resource {} from datpackage "
                    "with name {}".format(r.name, p.descriptor["name"])
                )
            )
    print("Successfully tested datapackage {}.".format(p.descriptor["name"]))


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
