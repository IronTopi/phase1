"""Implementation of the IDatabaseConnection interface for access to a MongoDB-instance."""
from typing import Dict, List, Any

from pydantic import BaseModel
from pymongo import MongoClient
from dataaccess.IDatabaseConnection import IDatabaseConnection, ItemNotFound


class MongoDatabaseConnection(IDatabaseConnection):
    """Implementation of the IDatabaseConnection interface for access to a MongoDB-instance."""

    def __init__(self, connectionData: Dict[str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """
        mongoConnectionData = MongoConnectionConfig.parse_obj(connectionData)

        self.Client = MongoClient(
            host=mongoConnectionData.IP,
            port=mongoConnectionData.Port,
            username=mongoConnectionData.User,
            password=mongoConnectionData.Password,
        )

        self.DB = self.Client[mongoConnectionData.Database]
        self.Collection = self.DB[mongoConnectionData.Collection]

        self._NextID = self._getMaxID()

    def _getMaxID(self) -> int:
        """Finds the max value of the already existing ids in the collection.

        Returns:
            int: Highest existing ID (or 0, if there are no items in the database yet)
        """
        maxID = 0

        if self.Collection.count_documents({}) > 0:
            maxID = self.Collection.find_one({}, {"id": 1}, sort=[("id", -1)])["id"]

        return maxID

    def _getNextID(self) -> int:
        """Returns next usable id.

        Returns:
            int: Next free id
        """
        self._NextID += 1
        return self._NextID

    def getAllItems(self) -> List[Dict]:
        return self.Collection.find({})

    def getItem(self, itemId: int):
        itemData = self.Collection.find_one({"id": itemId})

        if not itemData:
            raise ItemNotFound(f"item with id '{str(itemId)}' not found in database")

        return itemData

    def insertItem(self, itemData: Dict):
        # generate ID
        itemData["id"] = self._getNextID()

        # TODO: check if succeeded
        result = self.Collection.insert_one(itemData)

        return itemData

    def updateItem(self, itemData: Dict) -> Dict:
        result = self.Collection.update_one({"id": itemData["id"]}, {"$set": itemData})

        if result.matched_count != 1:
            raise ItemNotFound((f"item with id '{str( itemData['id'])}' not found in database"))

        return itemData

    def deleteItem(self, itemId: int):
        numberMatches = self.Collection.count_documents({"id": int(itemId)})
        if numberMatches == 0:
            raise ItemNotFound(f"item with id '{str(itemId)}' not found in database")

        self.Collection.delete_one({"id": int(itemId)})


class MongoConnectionConfig(BaseModel):
    """Connection data required for a MongoDB."""

    IP: str
    Port: int
    User: str
    Password: str

    Database: str
    Collection: str
