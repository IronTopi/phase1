from typing import Any, List, Dict
from abc import ABC

from api.models.City import City

class IDatabaseConnection (ABC):
    def __init__ (self, connectionData: Dict [str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """
        pass

    def getAllCities (self) -> List [City]:
        """Returns all stored cities.
        (No pagination!)

        Returns:
            List [City]: All cities as full models (not only id)
        """
        pass

    def updateCity (self, city: City):
        pass

    def insertCity (self, city: City):
        pass

    def deleteCity (self, city: City):
        pass
