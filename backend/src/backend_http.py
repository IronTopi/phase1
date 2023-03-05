from typing import List
import os


from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# TODO: move all domain-level validation out of the http-layer?
from pydantic import ValidationError

# TODO: remove, 

# DB-connection modules, might want to move the whole topic
from dataaccess.ItemDataRepository import ItemDataRepository, ItemNotFound
from dataaccess.MongoDatabaseConnection import (
    MongoDatabaseConnection,
    MongoConnectionConfig,
)

from api.models.Item import Item

app = FastAPI()
security = HTTPBasic()

ItemRepo: ItemDataRepository


@app.get("/items/")
def getAllItems() -> List[Item]:
    return ItemRepo.getAllItems()


@app.get("/items/{itemId}")
def read_item(
    itemId: int,
    credentials: HTTPBasicCredentials = Depends(security)
):
    try:
        return ItemRepo.getItem (itemId)

    except ValidationError as ve:
        raise HTTPException (500, detail=str (ve)) from ve

    except ItemNotFound as itemNotFound:
        raise HTTPException (404, detail=str (itemNotFound)) from itemNotFound



@app.post("/items/")
def createItem(item: Item, credentials: HTTPBasicCredentials = Depends(security)) -> Item:
    return ItemRepo.insertItem (item)


@app.put("/items/{itemId}")
def updateItem(itemId: int, item: Item, credentials: HTTPBasicCredentials = Depends(security)) -> Item:
    # TODO: allow partial input?
    # TODO: shitty design, we need id in url but dont use it
    # -> Best practice?!?!?
    try:
        return ItemRepo.updateItem (item)
    
    except ItemNotFound as itemNotFound:
        raise HTTPException (404, detail=str (itemNotFound)) from itemNotFound


@app.delete("/items/{itemId}")
def deleteItem(itemId: int, credentials: HTTPBasicCredentials = Depends(security)):
    try:
        ItemRepo.deleteItem (itemId)
    
    except ItemNotFound as itemNotFound:
        raise HTTPException (404, detail=str (itemNotFound)) from itemNotFound
    





##########
# Orchestration
# Set up underlying layers
@app.on_event("startup")
async def startup():
    # Setup repo
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
        print(
            f"ERROR - Database Connection - no valid configuration provided: missing env-var {str(ke)}"
        )
        exit(1)
