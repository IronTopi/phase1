"""Entry-point for the whole application.
Does some orchestration (dependencies) and runs the http-backend."""

from typing import List
import os
import logging

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from pydantic import ValidationError

from auth import validateCredentials

# DB-connection modules, might want to move the whole topic
from dataaccess.ItemDataRepository import ItemDataRepository, ItemNotFound
from dataaccess.MongoDatabaseConnection import (
    MongoDatabaseConnection,
    MongoConnectionConfig,
)

from api.models.Item import Item

DESCRIPTION = """
A simple CRUD-API.
"""

app = FastAPI(title="phase1 - mini-crud", description=DESCRIPTION, dependencies=[Depends(validateCredentials)])


ItemRepo: ItemDataRepository


@app.get("/items/")
async def getAllItems() -> List[Item]:
    """Lists all items.
    Returns complete items (not just ids).
    Does not do pagination.

    Returns:
        List[Item]: List of all items
    """
    return ItemRepo.getAllItems()


@app.get("/items/{itemId}")
async def readItem(itemId: int):
    """Returns the specified item

    Args:
        itemId (int): Id of the item to retrieve

    Raises:
        HTTPException: 404 if the item can not be found
        HTTPException: 500 if the item could be found but the data is invalid

    Returns:
        Item: The requested item
    """
    try:
        return ItemRepo.getItem(itemId)

    except ValidationError as ve:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ve)) from ve

    except ItemNotFound as itemNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(itemNotFound)) from itemNotFound


@app.post("/items/")
async def createItem(item: Item) -> Item:
    """Inserts a new item.

    Args:
        item (Item): Item to insert. Incoming item-id will be disregarded, actual id will be generated serverside.

    Raises:
        HTTPException: 422 if the item-data is malformed

    Returns:
        Item: The newly created item (including the actual id)
    """
    # Only thing that can go wrong is malformed data (validation error).
    # This is handeled by FastAPI, we won't even enter the function then.
    # Mention this case in docstring tho!
    return ItemRepo.insertItem(item)


@app.put("/items/{itemId}")
async def updateItem(itemId: int, item: Item) -> Item:
    """Updates the provided item

    Args:
        itemId (int): Id of the item to modify
        item (Item): New item data. Id cannot be changed

    Raises:
        HTTPException: 400 if the request tries to change the id (different id in URL and payload)
        HTTPException: 404 if the specified item does not exist

    Returns:
        Item: The modified item
    """
    # TODO: allow partial input -> use http.PATCH
    # Basic sanity check: do the itemIds in the route and the data match?
    if itemId != item.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f"item-id mismatch between route and payload")

    try:
        return ItemRepo.updateItem(item)

    except ItemNotFound as itemNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(itemNotFound)) from itemNotFound


@app.delete("/items/{itemId}")
async def deleteItem(itemId: int):
    """Deletes the specified item

    Args:
        itemId (int): Id of the item to delete

    Raises:
        HTTPException: 404 if the specified item does not exist
    """
    try:
        ItemRepo.deleteItem(itemId)

    except ItemNotFound as itemNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(itemNotFound)) from itemNotFound


##########
# Orchestration
# Set up underlying layers


@app.on_event("startup")
async def startup():
    # Setup Item-repo
    global ItemRepo

    # dependency injection
    dbConnection = setupMongoConnection()
    ItemRepo = ItemDataRepository(dbConnection)


def setupMongoConnection():
    try:
        # Get connection info using env-vars
        connectionConfig = MongoConnectionConfig(
            IP=os.environ["MONGO_IP"],
            Port=os.environ["MONGO_PORT"],
            User=os.environ["MONGO_USER"],
            Password=os.environ["MONGO_PASSWORD"],
            Database=os.environ["MONGO_DB"],
            Collection=os.environ["MONGO_COLLECTION"],
        )

        return MongoDatabaseConnection(connectionConfig)

    except KeyError as ke:
        logging.fatal(f"ERROR - Database Connection - no valid configuration provided: missing env-var {str(ke)}")
        exit(1)
