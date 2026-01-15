from oemof.network.network import Node

from oemof.tabular._facade import Facade


class Bus(Facade, Node):
    def __init__(self, label: str, **kwargs):
        super().__init__(label=label, **kwargs)

    def build_solph_components(self) -> None:
        pass
