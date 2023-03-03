from typing import Any, List
from abc import ABC

import api.models.City

class IDatabaseConnection (ABC):
    def __init__ (self, connectionData: Dict [str, Any]):
        """Connects this instance to the database configured in `connectionData`.

        Args:
            connectionData (Dict[str, Any]): Connection config (connection string), shape depends on specific database
        """

    def getAllCities (self) -> List [City]:
        """Returns all stored cities.
        (No pagination!)

        Returns:
            List [City]: All cities as full models (not only id)
        """

    def updateCity (self, city: City):

    def insertCity (self, city: City):

    def deleteCity (self, city: City):
