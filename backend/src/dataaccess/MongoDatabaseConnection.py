from typing import Dict, List, Any

from pydantic import BaseModel
from pymongo import MongoClient
from dataaccess.IDatabaseConnection import IDatabaseConnection

# TODO: remove, only Dict-data here!!!
from api.models.City import City

class MongoDatabaseConnection (IDatabaseConnection):
    def __init__ (self, connectionData: Dict [str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """
        # 
        mongoConnectionData = MongoConnectionConfig.parse_obj (connectionData)

        self.Client = MongoClient (host=mongoConnectionData.IP, port=mongoConnectionData.Port,username=mongoConnectionData.User, password=mongoConnectionData.Password )

        self.DB = self.Client [mongoConnectionData.Database]
        self.Collection = self.DB[mongoConnectionData.Collection]

        # TODO: make property?!
        self.NextID = self._getMaxID ()

    


    def _getMaxID (self) -> int:
        # db.things.find_one(sort=[("uid", pymongo.DESCENDING)])
        #highestId = self.Collection.find({}, {"id": 1}).sort("id",-1).limit(1)
        try:
            maxID = self.Collection.find_one({}, {"id": 1}, sort=[("id",-1)])["id"]
        
        except Exception as ex:
            # TODO: except only specific exception-type
            print (ex)
            maxID = 0

        return maxID
    
    def _getNextID (self) -> int:
        self.NextID += 1
        return self.NextID


    def getAllCities (self) -> List [Dict]:
        """Returns all stored cities.
        (No pagination!)
        """
        return self.Collection.find ({})
        

    def updateCity (self, d: City):
        pass

    def insertCity (self, city: Dict):
        # TODO: generate ID
        city ["id"] = self._getNextID()

        # TODO: check if succeeded
        self.Collection.insert_one (city)

        return city

    def deleteCity (self, city: City):
        pass



class MongoConnectionConfig (BaseModel):
    IP: str
    Port: int
    User: str
    Password: str

    Database: str
    Collection: str
