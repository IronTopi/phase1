from typing import List
import os
import logging

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# TODO: move all domain-level validation out of the http-layer?
# Introduce Domain-Exceptions ouside?
from pydantic import ValidationError

from auth import validateCredentials

# DB-connection modules, might want to move the whole topic
from dataaccess.ItemDataRepository import ItemDataRepository, ItemNotFound
from dataaccess.MongoDatabaseConnection import (
    MongoDatabaseConnection,
    MongoConnectionConfig,
)

from api.models.Item import Item

app = FastAPI(dependencies=[Depends (validateCredentials)])


ItemRepo: ItemDataRepository


@app.get("/items/")
def getAllItems() -> List[Item]:
    return ItemRepo.getAllItems()


@app.get("/items/{itemId}")
def readItem(
    itemId: int
):
    try:
        return ItemRepo.getItem (itemId)

    except ValidationError as ve:
        raise HTTPException (status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str (ve)) from ve

    except ItemNotFound as itemNotFound:
        raise HTTPException (status.HTTP_404_NOT_FOUND, detail=str (itemNotFound)) from itemNotFound



@app.post("/items/")
def createItem(item: Item) -> Item:
    return ItemRepo.insertItem (item)


@app.put("/items/{itemId}")
def updateItem(itemId: int, item: Item) -> Item:
    # TODO: allow partial input -> use http.PATCH
    try:
        return ItemRepo.updateItem (item)
    
    except ItemNotFound as itemNotFound:
        raise HTTPException (status.HTTP_404_NOT_FOUND, detail=str (itemNotFound)) from itemNotFound


@app.delete("/items/{itemId}")
def deleteItem(itemId: int):
    try:
        ItemRepo.deleteItem (itemId)
    
    except ItemNotFound as itemNotFound:
        raise HTTPException (status.HTTP_404_NOT_FOUND, detail=str (itemNotFound)) from itemNotFound
    





##########
# Orchestration
# Set up underlying layers
@app.on_event("startup")
async def startup():
    # Setup Item-repo
    global ItemRepo

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
        logging.fatal(
            f"ERROR - Database Connection - no valid configuration provided: missing env-var {str(ke)}"
        )
        exit(1)
