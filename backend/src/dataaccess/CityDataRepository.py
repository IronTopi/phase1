from typing import List

from dataaccess.IDatabaseConnection import IDatabaseConnection
from api.models.City import City

class CityDataRepository():
    def __init__(self, databaseConnection: IDatabaseConnection):
        self.DatabaseConnection = databaseConnection
        

    def getAllCities (self) -> List[City]:
        pass

    def insertCity (self, city: City) -> City:
        """Inserts city 'city'.

        Args:
            city (City): City to insert

        Returns:
            City: Newly inserted city
        """

        # TODO: Document exception that might occur on this level
        # validation of input-data should take place WHERE?
        # Here or here + in http-layer?
        pass
