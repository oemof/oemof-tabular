import abc
from dataclasses import dataclass

from oemof.solph.constraints.integral_limit import generic_integral_limit


class ConstraintFacade(abc.ABC):
    def build_constraint(self):
        pass


@dataclass
class EmissionConstraint(ConstraintFacade):
    name: str
    type: str
    emission_max: float
    keyword: str = "emission_factor"

    def build_constraint(self, model):
        # to use the constraints in oemof.solph, we need to pass the model.

        # check if there are flows with key
        flows = {}
        for (i, o) in model.flows:
            if hasattr(model.flows[i, o], self.keyword):
                flows[(i, o)] = model.flows[i, o]

        if not flows:
            raise Warning(f"No flows with keyword {self.keyword}")
        else:
            print(
                f"These flows will contribute to the "
                f"emission constraint {flows.keys()}"
            )

        # add constraint to the model
        generic_integral_limit(
            model, keyword=self.keyword, flows=flows, limit=self.emission_max
        )


CONSTRAINT_TYPE_MAP = {"emission_constraint": EmissionConstraint}
