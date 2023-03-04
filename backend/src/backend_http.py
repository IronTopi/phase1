from typing import List
import os


from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# DB-connection modules, might want to move the whole topic
from dataaccess.CityDataRepository import CityDataRepository
from dataaccess.MongoDatabaseConnection import (
    MongoDatabaseConnection,
    MongoConnectionConfig,
)

from api.models.City import City

app = FastAPI()
security = HTTPBasic()

ItemRepo: CityDataRepository


@app.get("/")
def getAllCities() -> List[City]:
    return ItemRepo.getAllCities()


@app.post("/")
def addCity(item: City, credentials: HTTPBasicCredentials = Depends(security)) -> City:
    return ItemRepo.insertCity (item)


@app.get("/items/{item_id}")
def read_item(
    item_id: int,
    q: str | None = None,
    credentials: HTTPBasicCredentials = Depends(security),
):
    return {"item_id": item_id, "q": q}


@app.get("/db-creds")
def getDbCredentials():
    return {
        "user": os.environ["MONGO_USER"],
        "password": os.environ["MONGO_PASSWORD"],
        "db": os.environ["MONGO_DB"],
        "collection": os.environ["MONGO_COLLECTION"],
    }


# Setup underlying layers
@app.on_event("startup")
async def startup():
    # Setup repo
    global ItemRepo

    dbConnection = setupMongoConnection()
    ItemRepo = CityDataRepository(dbConnection)


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
