from oemof.solph import Model
from dataclasses import dataclass

from oemof.solph.constraints.integral_limit import emission_limit

def add_subnodes(n, **kwargs):
    # ????
    deque((kwargs["Model"].add(sn) for sn in n.subnodes), maxlen=0)


class ConstraintFacade():
    __init__(self):
        Model.signals[EnergySystem.add].connect(
            add_constraint_blocks, sender=self
        )


@dataclass
class EmissionConstraint(ConstraintFacade):
    emission_min: float
    emission_max: float
    flow_keyword: str

    def build_constraint(self, model):
        # to use the constraints in oemof.solph, we need to pass the model.
        emission_limit(model, flows=None, limit=self.emission_max)


CONSTRAINT_TYPE_MAP = {
    "emission_constraint": EmissionConstraint
}
