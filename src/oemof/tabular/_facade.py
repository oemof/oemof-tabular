# -*- coding: utf-8 -*-

"""Facade's are classes providing a simplified view on more complex classes.

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
import warnings
from abc import abstractmethod
from collections.abc import Iterable

import numpy as np
from oemof.solph import Investment
from oemof.solph.components import GenericStorage, Link
from oemof.tools.debugging import SuspiciousUsageWarning

# Switch off SuspiciousUsageWarning
warnings.filterwarnings("ignore", category=SuspiciousUsageWarning)


class Facade:
    """
    Parent class for oemof.tabular facades.
    """

    def __init__(self, **kwargs):
        """ """

        self.mapped_type = type(self)

        self.type = kwargs.get("type")

        allowed_kwargs = self.__get_allowed_kwargs_from_solph_component(
            **kwargs
        )
        super().__init__(**allowed_kwargs)

        self.build_solph_components()

    def __get_allowed_kwargs_from_solph_component(self, **kwargs):
        """
        Read allowed paramaters of related oemof.solph component.

        Store parameters which are not present in "custom_properties" if
        exists.
        """
        # Get the signature of the parent class __init__
        import inspect

        parent_class = super(Facade, self)
        parent_init = parent_class.__init__

        # Get allowed parameters for parent __init__
        try:
            sig = inspect.signature(parent_init)
            allowed_params = set(sig.parameters.keys()) - {"self"}
        except (ValueError, TypeError):
            # If we can't get signature, assume all kwargs are allowed
            allowed_params = set(kwargs.keys())

        # Always allow "label":
        allowed_params = allowed_params | {"label"}

        # Split kwargs into allowed and custom
        allowed_kwargs = {}
        custom_properties = {}

        for key, value in kwargs.items():
            if key in allowed_params:
                allowed_kwargs[key] = value
            else:
                custom_properties[key] = value

        # Pass allowed kwargs to super and store custom properties if allowed
        if custom_properties and "custom_properties" in allowed_params:
            allowed_kwargs["custom_properties"] = custom_properties

        return allowed_kwargs

    def _nominal_capacity(self):
        """Returns investment if self.expandable ist True otherwise it returns
        the capacity
        """
        if self.expandable is True:
            return self._investment()

        else:
            if isinstance(self, Link):
                return {
                    "from_to": self.from_to_capacity,
                    "to_from": self.to_from_capacity,
                }
            else:
                return self.capacity

    def _investment(self):
        if self.capacity_cost is None:
            msg = (
                "If you set `expandable`to True you need to set "
                "attribute `capacity_cost` of component {}!"
            )
            raise ValueError(msg.format(self.label))
        # If storage component
        if isinstance(self, GenericStorage):
            # If invest costs/MWH are given
            if self.storage_capacity_cost is not None:
                return Investment(
                    ep_costs=self.storage_capacity_cost,
                    maximum=self._get_maximum_additional_invest(
                        "storage_capacity_potential", "storage_capacity"
                    ),
                    minimum=getattr(self, "minimum_storage_capacity", 0),
                    existing=getattr(self, "storage_capacity", 0),
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                    fixed_costs=getattr(self, "fixed_costs", None),
                )
            # If invest costs/MWh are not given
            else:
                return Investment(
                    maximum=self._get_maximum_additional_invest(
                        "storage_capacity_potential", "storage_capacity"
                    ),
                    minimum=getattr(self, "minimum_storage_capacity", 0),
                    existing=getattr(self, "storage_capacity", 0),
                    lifetime=getattr(self, "lifetime", None),
                    age=getattr(self, "age", 0),
                    fixed_costs=getattr(self, "fixed_costs", None),
                )
        # If other component than storage
        else:
            return Investment(
                ep_costs=self.capacity_cost,
                maximum=self._get_maximum_additional_invest(
                    "capacity_potential", "capacity"
                ),
                minimum=getattr(self, "capacity_minimum", 0),
                existing=getattr(self, "capacity", 0),
                lifetime=getattr(self, "lifetime", None),
                age=getattr(self, "age", 0),
                fixed_costs=getattr(self, "fixed_costs", None),
            )

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

        if isinstance(_potential, Iterable) and not isinstance(
            _existing, Iterable
        ):
            _existing = [_existing] * len(_potential)
        if isinstance(_existing, Iterable) and not isinstance(
            _potential, Iterable
        ):
            _potential = [_potential] * len(_existing)
        maximum = np.array(_potential) - np.array(_existing)

        if bool(maximum.min() < 0):
            raise ValueError(
                f"Existing {attr_existing}={_existing} is larger"
                f" than {attr_potential}={_potential}."
            )

        return maximum

    def update(self):
        self.build_solph_components()

    @abstractmethod
    def build_solph_components(self) -> None:
        raise NotImplementedError("Must be implemented by facade.")
