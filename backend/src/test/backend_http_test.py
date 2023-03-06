"""Test all API routes, down to the persistence layer.

DANGER:
This will put some trash into your database and modify existing items!!!"""

import random

import pytest
from fastapi.testclient import TestClient
from auth import validateCredentials

from backend_http import app

print (app)

@pytest.fixture()
def client ():
    app.dependency_overrides [validateCredentials] = lambda: True
    with TestClient (app) as _client:
        yield _client


def test_getAllItems (client: TestClient):
    response = client.get ("/items/")
    assert response.status_code == 200

def test_getItem_Good (client: TestClient):
    response = client.get ("/items/")
    assert response.status_code == 200

    # Select one random item
    allItems = response.json()

    # Assume we have some entries. Might add those in a fixture.
    item = random.choice (allItems)
    response = client.get (f"/items/{item['id']}")
    assert response.status_code == 200


def test_getItem_Bad (client: TestClient):
    # There should be no Item with a negative id
    response = client.get ("/items/-1")
    assert response.status_code == 404


def test_createItem_Good (client: TestClient):
    # Create good Item

    # TODO: randomize data
    response = client.post(
        "/items/",
        json={"id": -1, 
              "city": "ankh morpork", 
              "start_date": "1/3/1999",
              "end_date": "1/12/2020",
              "price": "13.37",
              "status": "Daily",
              "color": "#Aa1234"},
    )

    assert response.status_code == 200

    # Did we ge a useful ID back?
    assert response.json() ["id"] > 0

def test_createItem_Bad (client: TestClient):
    # Create item with malformed data
    response = client.post(
        "/items/",
        json={"id": -1, 
              "city": "ankh morpork", 
              "start_date": "1/3/1999",
              "end_date": "1/12/2020",
              "price": "13.37",
              "status": "Daily",
              "color": "blue"},
    )
    assert response.status_code == 422


def test_updateItem (client: TestClient):
    response = client.get ("/items/")
    assert response.status_code == 200

    # Select one random item
    allItems = response.json()

    # Assume we have some entries. Might add those in a fixture.
    item = random.choice (allItems)
    item ["city"] = item ["city"]*2
    # Modify item
    response = client.put(
        f"/items/{item['id']}",
        json=item
    )
    
    assert response.status_code == 200
    assert response.json() == item


def test_deleteItem (client: TestClient):
    # Create good Item and then delete it

    # TODO: randomize data
    response = client.post(
        "/items/",
        json={"id": -1, 
              "city": "ankh morpork", 
              "start_date": "1/3/1999",
              "end_date": "1/12/2020",
              "price": "13.37",
              "status": "Daily",
              "color": "#Aa1234"},
    )

    assert response.status_code == 200
    itemId = response.json() ["id"]

    response = client.delete (f"/items/{itemId}")
    assert response.status_code == 200