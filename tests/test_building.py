import pandas as pd
from oemof.solph.helpers import extend_basic_path

from oemof.tabular.datapackage import building


def test_create_default_datapackage():

    building.create_default_datapackage(
        "default_datapackage",
        extend_basic_path("tmp"),
        datetimeindex=pd.date_range("1/1/2016", periods=24 * 10, freq="H"),
        components={
            "ch4-gt": {"type": "conversion", "carrier": "ch4"},
            "wind-onshore": {"type": "volatile", "carrier": "wind"},
        },
        busses=None,
        regions=None,
        links=None,
    )


def test_get_facade_fields():
    building.get_facade_fields()


test_create_default_datapackage()
