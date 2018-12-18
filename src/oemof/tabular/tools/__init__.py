""" `oemof.tabular`'s kitchen sink module.

Contains all the general tools needed by other tools dealing with specific
tabular data sources.
"""

import types
from oemof.tabular.tools.datapackage import building, processing, aggregation

class HSN(types.SimpleNamespace):
    """ A hashable variant of `types.Simplenamespace`.

    By making it hashable, we can use the instances as dictionary keys, which
    is necessary, as this is the default type for flows.
    """
    def __hash__(self):
        return id(self)


def raisestatement(exception, message=""):
    """ A version of `raise` that can be used as a statement.
    """
    if message:
        raise exception(message)
    else:
        raise exception()


def remap(mapping, renamings, selection):
    """ Change `mapping`'s keys according to the `selection` in `renamings`.

    The `renaming` found under `selection` in `renamings` is used to rename the
    keys found in `mapping`. I.e., return a copy of `mapping` with every `key`
    of `mapping` that is also found in `renaming` replaced with
    `renaming[key]`.

    If key doesn't have a renaming, it's returned as is. If `selection` doesn't
    appear as a key in `renamings`, `mapping` is returned unchanged.

    Example:
    --------
    >>> renamings = {'R1': {'zero': 'nada'}, 'R2': {'foo': 'bar'}}
    >>> mapping = {'zero': 0, 'foo': 'foobar'}
    >>> remap(mapping, renamings, 'R1') == {'nada': 0, 'foo': 'foobar'}
    True
    >>> remap(mapping, renamings, 'R2') == {'zero': 0, 'bar': 'foobar'}
    True

    As a special case, if `selection` is a `class`, not only `selection` is
    considered to select a renaming, but the classes in `selection`'s `mro` are
    considered too. The first class in `selection`'s `mro` which is also found
    to be a key in `renamings` is used to determine which renaming to use. The
    search starts at `selection`.


    Parameters
    ----------
    mapping: `Mapping`
        The `Mapping` whose keys should be renamed.
    renamings: `Mapping` of `Mappings <collections.abc.Mapping>`
    selection: `Hashable`
        Key specifying which entry in `renamings` is used to determine the new
        keys in the copy of `mapping`. If `selection` is a `class`, the first
        entry of `selection`'s `mro` which is found in `renamings` is used to
        determine the new keys.
    """
    mro = getattr(selection, "mro", lambda: [selection])
    for c in mro():
        if c in renamings:
            break
    return {renamings.get(c, {}).get(k, k): v for k, v in mapping.items()}
