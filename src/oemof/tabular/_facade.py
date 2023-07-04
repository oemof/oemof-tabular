# -*- coding: utf-8 -*-

""" Facade's are classes providing a simplified view on more complex classes.

More specifically, the `Facade`s in this module act as simplified, energy
specific  wrappers around `oemof`'s and `oemof.solph`'s more abstract and
complex classes. The idea is to be able to instantiate a `Facade` using keyword
arguments, whose value are derived from simple, tabular data sources. Under the
hood the `Facade` then uses these arguments to construct an `oemof` or
`oemof.solph` component and sets it up to be easily used in an `EnergySystem`.

**Note** The mathematical notation is as follows:

* Optimization variables (endogenous variables) are denoted by :math:`x`
* Optimization parameters (exogenous variables) are denoted by :math:`c`
* The set of timesteps :math:`T` describes all timesteps of the optimization
  problem

SPDX-License-Identifier: BSD-3-Clause
"""
import dataclasses
import inspect
import warnings
from collections import deque
from dataclasses import dataclass

from oemof.network.energy_system import EnergySystem
from oemof.network.network import Node
from oemof.solph import Investment
from oemof.solph.components import GenericStorage, Link
from oemof.tools.debugging import SuspiciousUsageWarning

# Switch off SuspiciousUsageWarning
warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)


def kwargs_to_parent(cls):
    r"""
    Decorates the __init__ of a given class by first
    passing args and kwargs to the __init__ of the parent
    class.

    Parameters
    ----------
    cls : Class with an __init__ to decorate

    Returns
    -------
    cls : Class with decorated __init__
    """
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        # pass only those kwargs to the dataclass which are expected
        dataclass_kwargs = {
            key: value
            for key, value in kwargs.items()
            if key in [f.name for f in dataclasses.fields(cls)]
        }

        # pass args and kwargs to the dataclasses' __init_
        original_init(self, *args, **dataclass_kwargs)

        # update kwargs with default arguments
        kwargs.update(dataclasses.asdict(self))

        # Pass only those arguments to solph component's __init__ that
        # are expected.
        init_expected_args = list(
            inspect.signature(super(cls, self).__init__).parameters
        )

        kwargs_expected = {
            key: value
            for key, value in kwargs.items()
            if key in init_expected_args
        }

        kwargs_unexpected = {
            key: value
            for key, value in kwargs.items()
            if key not in init_expected_args
        }

        if "custom_attributes" in init_expected_args:
            kwargs_expected["custom_attributes"] = kwargs_unexpected

        if kwargs_unexpected and "custom_attributes" not in init_expected_args:
            warnings.warn(
                f"No custom_attributes in parent class {cls.__mro__[1]}"
            )

        super(cls, self).__init__(
            **kwargs_expected,
        )

        if not kwargs.get("build_solph_components") is False:
            self.build_solph_components()

    cls.__init__ = new_init
    return cls


def dataclass_facade(cls):
    r"""
    Decorates a facade class by first as a
    dataclass, taking care of args and kwargs
    in the __init__

    Parameters
    ----------
    cls : facade class

    Returns
    -------
    cls : facade class
    """
    assert issubclass(cls, Facade)

    # First, decorate as dataclass.
    # The settings are important to not override the __hash__ method
    # defined in oemof.network.Node
    cls = dataclass(cls, unsafe_hash=False, frozen=False, eq=False)

    # Second, decorate to handle kwargs in __init__
    cls = kwargs_to_parent(cls)

    return cls


def add_subnodes(n, **kwargs):
    deque((kwargs["EnergySystem"].add(sn) for sn in n.subnodes), maxlen=0)


class Facade(Node):
    """
    Parent class for oemof.tabular facades.
    """

    def __init__(self, *args, **kwargs):
        """ """

        self.mapped_type = type(self)

        self.type = kwargs.get("type")

        super().__init__(*args, **kwargs)

        self.subnodes = []
        EnergySystem.signals[EnergySystem.add].connect(
            add_subnodes, sender=self
        )

    def _nominal_value(self):
        """Returns None if self.expandable ist True otherwise it returns
        the capacity
        """
        if self.expandable is True:
            if isinstance(self, Link):
                return {"from_to": None, "to_from": None}
            else:
                return None

        else:
            if isinstance(self, Link):
                return {
                    "from_to": self.from_to_capacity,
                    "to_from": self.to_from_capacity,
                }
            else:
                return self.capacity

    def _investment(self):
        if not self.expandable:
            self.investment = None
            return self.investment
        if self.capacity_cost is None:
            msg = (
                "If you set `expandable`to True you need to set "
                "attribute `capacity_cost` of component {}!"
            )
            raise ValueError(msg.format(self.label))
        if isinstance(self, GenericStorage):
            if self.storage_capacity_cost is not None:
                self.investment = Investment(
                    ep_costs=self.storage_capacity_cost,
                    maximum=self._get_maximum_additional_invest(
                        "storage_capacity_potential", "storage_capacity"
                    ),
                    minimum=getattr(self, "minimum_storage_capacity", 0),
                    existing=getattr(self, "storage_capacity", 0),
                )
            else:
                self.investment = Investment(
                    maximum=self._get_maximum_additional_invest(
                        "storage_capacity_potential", "storage_capacity"
                    ),
                    minimum=getattr(self, "minimum_storage_capacity", 0),
                    existing=getattr(self, "storage_capacity", 0),
                )
        else:
            self.investment = Investment(
                ep_costs=self.capacity_cost,
                maximum=self._get_maximum_additional_invest(
                    "capacity_potential", "capacity"
                ),
                minimum=getattr(self, "capacity_minimum", 0),
                existing=getattr(self, "capacity", 0),
                lifetime=getattr(self, "lifetime", None),
            )
        return self.investment

    def _get_maximum_additional_invest(self, attr_potential, attr_existing):
        r"""
        Calculates maximum additional investment by
        substracting existing from potential.

        Throws an error if existing is larger than potential.
        """
        _potential = getattr(self, attr_potential, float("+inf"))
        _existing = getattr(self, attr_existing, 0)

        if _existing is None:
            _existing = 0

        if _potential is None:
            _potential = float("+inf")

        maximum = _potential - _existing

        if maximum < 0:
            raise ValueError(
                f"Existing {attr_existing}={_existing} is larger"
                f" than {attr_potential}={_potential}."
            )

        return maximum

    def update(self):
        self.build_solph_components()
