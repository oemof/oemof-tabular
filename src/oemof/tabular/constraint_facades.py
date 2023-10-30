import abc
from dataclasses import dataclass

from oemof.solph.constraints.integral_limit import generic_integral_limit
from pyomo.environ import Constraint

from oemof.tabular.facades import Bev


def var2str(var):
    return "_".join(
        [i.label if not isinstance(i, int) else str(i) for i in var]
    )


def get_bev_label(var):
    return var[1].label.split("-storage")[0]


def get_period(model, year, constraint_type=None):
    if model.es.periods:
        years = [period.year.min() for period in model.es.periods]
        for period_index, period_year in enumerate(years):
            if period_year == year:
                return period_index
        raise ValueError(
            f"'{constraint_type}' constraint facade:\n"
            f"Year {year} is not in model.PERIODS."
        )
    elif year == model.es.timeindex.year.min():
        return 0
    else:
        raise ValueError(
            f"'{constraint_type}' constraint facade:\n"
            f"Year {year} is not in model.timeindex."
        )


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


@dataclass
class BevShareMob(ConstraintFacade):
    name: str
    type: str
    year: int
    label: str
    share_mob_flex_G2V: (int, float)
    share_mob_flex_V2G: (int, float)
    share_mob_inflex: (int, float)

    @staticmethod
    def map_share2vars(model, share_mob, period):
        invest_vars = []
        for node in model.es.nodes:
            if isinstance(node, Bev):
                invest_vars.extend(
                    [
                        inv
                        for inv in model.InvestmentFlowBlock.invest
                        if node.electricity_bus.label == inv[0].label
                        and f"{node.facade_label}-storage" in inv[1].label
                        and period == inv[2]
                    ]
                )

        share_mob = {
            inv_var: value
            for key, value in share_mob.items()
            for inv_var in invest_vars
            if key in inv_var[1].label
        }
        return invest_vars, share_mob

    @staticmethod
    def convert_share(share):
        if 0 <= share <= 1:
            return share
        elif 0 <= share <= 100:
            return share / 100
        else:
            raise ValueError(f"Mob share: {share} not in [0,1] or [0,100]")

    def build_constraint(self, model):
        period = get_period(model, self.year, self.__class__.__name__)

        if period > len(model.PERIODS):
            raise ValueError(
                f"Period {period} not in model.PERIODS {model.PERIODS}"
            )

        share_mob = {
            f"{self.label}-G2V-storage": self.convert_share(
                self.share_mob_flex_G2V
            ),
            f"{self.label}-V2G-storage": self.convert_share(
                self.share_mob_flex_V2G
            ),
            f"{self.label}-inflex-storage": self.convert_share(
                self.share_mob_inflex
            ),
        }

        invest_vars, share_mob = self.map_share2vars(
            model=model, share_mob=share_mob, period=period
        )

        def investment_constraints_rule(InvestmentFlowBlock):
            return InvestmentFlowBlock.invest[inv_var] == share_mob[
                inv_var
            ] * sum(InvestmentFlowBlock.invest[iv] for iv in invest_vars)

        for inv_var in invest_vars:
            name = f"mob_share_{get_bev_label(inv_var)}_{period}"
            setattr(
                model.InvestmentFlowBlock,
                name,
                Constraint(rule=investment_constraints_rule),
            )


@dataclass
class BevEqualInvest(ConstraintFacade):
    name: str
    type: str
    year: int

    @staticmethod
    def double_with_offset(lst):
        result = []
        for i in range(len(lst) - 1):
            result.append((lst[i], lst[i + 1]))
        return result

    @staticmethod
    def get_bev_invest_vars(model, period):
        all_invest_vars = {}
        for node in model.es.nodes:
            if isinstance(node, Bev):
                invest_vars_bev = list(
                    set(
                        inv
                        for inv in model.InvestmentFlowBlock.invest
                        if inv[2] == period
                        for edge in inv[:2]
                        if node.facade_label in edge.label
                    )
                )
                all_invest_vars[node.facade_label] = invest_vars_bev
        return all_invest_vars

    def build_constraint(self, model):
        # TODO add checks
        period = get_period(model, self.year, self.__class__.__name__)
        if period > len(model.PERIODS):
            raise ValueError(
                f"Period {period} not in model.PERIODS {model.PERIODS}"
            )

        invest_vars = self.get_bev_invest_vars(model, period)

        def equate_variables_rule(InvestmentFlowBlock):
            return (
                InvestmentFlowBlock.invest[var1]
                == InvestmentFlowBlock.invest[var2]
            )

        for bev_label, invest_vars in invest_vars.items():
            for i, (var1, var2) in enumerate(
                self.double_with_offset(invest_vars)
            ):
                name = f"{bev_label}_equal_invest_{i}_({period})"
                setattr(
                    model.InvestmentFlowBlock,
                    name,
                    Constraint(rule=equate_variables_rule),
                )


CONSTRAINT_TYPE_MAP = {
    "generic_integral_limit": GenericIntegralLimit,
    "bev_equal_invest": BevEqualInvest,
    "bev_share_mob": BevShareMob,
}
