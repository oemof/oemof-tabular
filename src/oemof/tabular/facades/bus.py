from oemof.network.network import Bus

from oemof.tabular._facade import Facade


class Bus(Facade, Bus):
    def __init__(self, label: str, **kwargs):
        super().__init__(label=label, **kwargs)

    def build_solph_components(self) -> None:
        pass
