import abc
from dataclasses import dataclass

from oemof.solph.constraints.integral_limit import generic_integral_limit
from oemof.solph.constraints.equate_variables import equate_variables


class ConstraintFacade(abc.ABC):
    def build_constraint(self):
        pass


@dataclass
class GenericIntegralLimit(ConstraintFacade):
    name: str
    type: str
    limit: float
    keyword: str = "emission_factor"

    def build_constraint(self, model):
        # to use the constraints in oemof.solph, we need to pass the model.

        # check if there are flows with key
        flows = {}
        for i, o in model.flows:
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
            model, keyword=self.keyword, flows=flows, limit=self.limit
        )


CONSTRAINT_TYPE_MAP = {"generic_integral_limit": GenericIntegralLimit}


# @dataclass
# class JointExtension(ConstraintFacade):
#     name: str
#     type: str
#     limit: float
#     keyword: str = "joint_extension"
#
#
#     def build_constraint(self, model):
#         # components = {}
#         # for i in model.NODES:
#         #     if hasattr(model.NODES[i], self.keyword):
#         #         components[(i, o)] = model.NODES[i]
#         components = {i: model.NODES[i] for i in model.NODES if
#                       hasattr(model.NODES[i], self.keyword)}
#
#         if not components:
#             raise Warning(f"No components with keyword {self.keyword}")
#         else:
#             print(
#                 "These components will be extended jointly: "
#                 f"{components.keys()}"
#             )
#
#         # add constraint to the model
#         equate_variables(
#             model,
#             var1=model.InvestmentFlowBlock.invest[],
#             var2=)
