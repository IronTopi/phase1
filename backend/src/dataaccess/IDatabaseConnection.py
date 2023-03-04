"""Interface to the persistence layer.
Sends/Receives data in a generic structure (Dict) to the upper (domain) level."""
from typing import Any, List, Dict
from abc import ABC



class IDatabaseConnection (ABC):
    def __init__ (self, connectionData: Dict [str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """
        pass

    def getAllCities (self) -> List [Dict]:
        """Returns all stored cities.
        (No pagination!)

        Returns:
            List [City]: All cities as full models (not only id)
        """
        # TODO: raise NotImplemented? Or what's best practice for ABCs?
        pass
    
    def getCity (self, id: int) -> Dict:
        pass

    def updateCity (self, itemData: Dict):
        pass

    def insertCity (self, itemData: Dict):
        pass

    def deleteCity (self, id: int):
        pass
