from typing import Dict, Any

import pytest
from pydantic import ValidationError

from api.models.Item import Item


def buildGoodItem() -> Item:
    """Builds an item that should validate without errors.

    Returns:
        Item: good item
    """
    return {
        "id": -1,
        "city": "ankh morpork",
        "start_date": "1/3/1999",
        "end_date": "1/12/2020",
        "price": "13.37",
        "status": "Daily",
        "color": "#Aa1234",
    }


def test_createItem_Good():
    rawData = buildGoodItem()
    Item.parse_obj(rawData)


@pytest.mark.parametrize(
    "badAttribute,badValue",
    [("start_date", "2023-01-01"), ("end_date", "20.3.2021"), ("price", "12,74 €"), ("color", "red")],
)
def test_createItem_BadAttribute(badAttribute: str, badValue: Any):
    """Takes a good item and modifies the specified attribute.
    Should be used to inject one known bad value for each attribute.

    Args:
        badAttribute (Dict[str, Any]): `attribute_name` -> `attribute_value`
    """
    # city and status will not be tested, their type is str and pydantic can convert anything to a string

    rawData = buildGoodItem()
    rawData[badAttribute] = badValue

    with pytest.raises(ValidationError) as info:
        Item.parse_obj(rawData)


@pytest.mark.parametrize("attributeToOmit", [("city"), ("start_date"), ("end_date"), ("price"), ("status"), ("color")])
def test_createItem_MissingAttribute(attributeToOmit: str):
    rawData = buildGoodItem()
    del rawData[attributeToOmit]

    with pytest.raises(ValidationError) as info:
        Item.parse_obj(rawData)
