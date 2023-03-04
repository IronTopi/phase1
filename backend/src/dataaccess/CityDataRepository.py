from typing import List, Dict

from dataaccess.IDatabaseConnection import IDatabaseConnection
from api.models.City import City
from pydantic import ValidationError 

class CityDataRepository():
    def __init__(self, databaseConnection: IDatabaseConnection):
        self.DatabaseConnection = databaseConnection
        

    def getAllCities (self) -> List[City]:
        rawItems = self.DatabaseConnection.getAllCities()
        items = []

        for item in rawItems:
            try:
                print (item)
                items.append (City.parse_obj (item))
            
            except Exception as ex:
                print (ex)
        
        return items

    def insertCity (self, itemData: City):
        """_summary_

        Args:
            itemData (Dict): _description_
        """
        # TODO: Document exception that might occur on this level
        # validation of input-data should take place WHERE?
        # Here or here + in http-layer?


        
        # TODO: error-handling
        # ID will be generated in persistence layer
        insertedData = self.DatabaseConnection.insertCity (itemData.dict())
        return City.parse_obj (insertedData)
        


