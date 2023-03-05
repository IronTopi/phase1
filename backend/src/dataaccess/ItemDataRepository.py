from typing import List, Dict

#from dataaccess.IDatabaseConnection import IDatabaseConnection, ItemNotFound
import dataaccess.IDatabaseConnection as IDatabaseConnection
from api.models.Item import Item
from pydantic import ValidationError 

class ItemDataRepository():
    def __init__(self, databaseConnection: IDatabaseConnection.IDatabaseConnection):
        self.DatabaseConnection = databaseConnection
        

    def getAllItems (self) -> List[Item]:
        rawItems = self.DatabaseConnection.getAllItems()
        items = []

        for item in rawItems:
            # Fill the list as best as we can!
            try:
                print (item)
                items.append (Item.parse_obj (item))
            
            except Exception as ex:
                # TODO: simple logging
                print (ex)
        
        return items

    def getItem (self, itemId: int) -> Item:
        try:
            rawData = self.DatabaseConnection.getItem (itemId)
            item = Item.parse_obj (rawData)

        except ValidationError as ve:
            raise ve

        except IDatabaseConnection.ItemNotFound as itemNotFound:
            raise ItemNotFound (str(itemNotFound)) from itemNotFound

        
        return item



    def insertItem (self, itemData: Item):
        """_summary_

        Args:
            itemData (Dict): _description_
        """
        # TODO: Document exception that might occur on this level
        # validation of input-data should take place WHERE?
        # Here or here + in http-layer?


        
        # TODO: error-handling
        # ID will be generated in persistence layer
        insertedData = self.DatabaseConnection.insertItem (itemData.dict())
        return Item.parse_obj (insertedData)
        
    def updateItem (self, itemData: Item):
        try:
            self.DatabaseConnection.updateItem (itemData.dict())
            return itemData
        
        except IDatabaseConnection.ItemNotFound as itemNotFound:
            raise ItemNotFound (str(itemNotFound)) from itemNotFound

    def deleteItem (self, itemId: int):
        try:
            self.DatabaseConnection.deleteItem (itemId)
            
        except IDatabaseConnection.ItemNotFound as itemNotFound:
            raise ItemNotFound (str(itemNotFound)) from itemNotFound


class ItemNotFound (Exception):
    pass