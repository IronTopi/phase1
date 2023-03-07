"""Interface to the persistence layer.
Exchanges data with the the upper (domain) level in a generic structure (Dict)."""

from typing import Any, List, Dict
from abc import ABC, abstractmethod


class IDatabaseConnection(ABC):
    def __init__(self, connectionData: Dict[str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """
        pass

    @abstractmethod
    def getAllItems(self) -> List[Dict]:
        """Returns all stored items.
        (No pagination!)

        Returns:
            List [Item]: All items as full models (not only id)
        """
        pass

    @abstractmethod
    def getItem(self, itemId: int) -> Dict:
        """Returns specified item.

        Args:
            itemId (int): Identifier of the item to retrieve

        Returns:
            Dict: Item data
        """
        pass

    @abstractmethod
    def insertItem(self, itemData: Dict):
        """Inserts item.

        Args:
            itemData (Dict): New item data
        """
        pass

    @abstractmethod
    def updateItem(self, itemData: Dict) -> Dict:
        """Updates specified item.

        Args:
            itemData (Dict): New item data

        Returns:
            Dict: New item data
        """
        pass

    @abstractmethod
    def deleteItem(self, itemId: int):
        """Removes specified item.

        Args:
            itemId (int): Id of the item to delete
        """
        pass


# TODO: move to api.Errors
class ItemNotFound(Exception):
    """Specified item does not exist."""

    pass
