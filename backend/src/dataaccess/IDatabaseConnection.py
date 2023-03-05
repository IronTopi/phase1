"""Interface to the persistence layer.
Sends/Receives data in a generic structure (Dict) to the upper (domain) level."""
from typing import Any, List, Dict
from abc import ABC, abstractmethod



class IDatabaseConnection (ABC):
    def __init__ (self, connectionData: Dict [str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """
        pass

    @abstractmethod
    def getAllItems (self) -> List [Dict]:
        """Returns all stored items.
        (No pagination!)

        Returns:
            List [Item]: All items as full models (not only id)
        """
        pass
    
    @abstractmethod
    def getItem (self, id: int) -> Dict:
        pass


    @abstractmethod
    def insertItem (self, itemData: Dict):
        pass

    @abstractmethod
    def updateItem (self, itemData: Dict):
        pass


    @abstractmethod
    def deleteItem (self, id: int):
        pass

class ItemNotFound (Exception):
    pass