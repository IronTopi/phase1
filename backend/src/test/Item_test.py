import pytest
from pydantic import ValidationError

from api.models.Item import Item


def test_createItem_Good():
    rawData = {
        "id": -1,
        "city": "ankh morpork",
        "start_date": "1/3/1999",
        "end_date": "1/12/2020",
        "price": "13.37",
        "status": "Daily",
        "color": "#Aa1234",
    }

    Item.parse_obj(rawData)


def test_createItem_Bad():
    rawData = {
        "id": -1,
        "city": "ankh morpork",
        "start_date": "1/3/1999",
        "end_date": "1/12/2020",
        "price": "13.37",
        "status": "Daily",
        "color": "blue",
    }
    with pytest.raises(ValidationError) as e_info:
        Item.parse_obj(rawData)
