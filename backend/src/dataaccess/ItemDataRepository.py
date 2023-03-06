"""Accepts and delivers domain models in and out of persistence.

Is _not_ designed as an interface!
(But might be, could be useful to do a more isolated unit-test on the API)
We can still provide mock-datasources for testing because the 'databaseConnection' this
repo uses is designed as an interface.

The connection to the actual persistence layer uses an interface (IDatabaseConnection).
The repository and the actual database connection are not integrated into one single unit
to allow for domain entities to have their data split into multiple data-stores on the persistence layer.
The repository would then assemble the whole aggregate, do hydration-work etc.
"""

from typing import List
import logging

import dataaccess.IDatabaseConnection as IDatabaseConnection
from api.models.Item import Item
from pydantic import ValidationError 

class ItemDataRepository():
    """Repository for domain-models of the type 'Item'.
    """
    def __init__(self, databaseConnection: IDatabaseConnection.IDatabaseConnection):
        """Init this DataRepository.

        Args:
            databaseConnection (IDatabaseConnection.IDatabaseConnection): Database connection to use
        """
        self.DatabaseConnection = databaseConnection
        

    def getAllItems (self) -> List[Item]:
        """Returns list of all items.
        Any items that could not be loaded (-> validation error) are logged
        but not contained in the result.
        
        Returns:
            List[Item]: All items
        """
        rawItems = self.DatabaseConnection.getAllItems()
        items = []

        for item in rawItems:
            # Fill the list as best as we can!
            try:
                items.append (Item.parse_obj (item))
            
            except Exception as ex:
                logging.error (str(ex))
        
        return items

    def getItem (self, itemId: int) -> Item:
        """Returns item identified by 'itemId'.

        Args:
            itemId (int): Id of the item to receive

        Raises:
            ValidationError: Malformed data in persistence layer
            ItemNotFound: No item with id 'itemId' found

        Returns:
            Item: Item with id 'itemId'
        """
        try:
            rawData = self.DatabaseConnection.getItem (itemId)
            item = Item.parse_obj (rawData)

        except ValidationError as ve:
            logging.error (str(ve))
            raise ve

        except IDatabaseConnection.ItemNotFound as itemNotFound:
            raise ItemNotFound (str(itemNotFound)) from itemNotFound

        return item



    def insertItem (self, itemData: Item):
        """Inserts item into persistence.

        Args:
            itemData (Item): Item so save
        """        
        # Round-trip to get actual id (generated in database-connection)
        insertedData = self.DatabaseConnection.insertItem (itemData.dict())
        return Item.parse_obj (insertedData)
        
    def updateItem (self, itemData: Item) -> Item:
        """Modifies item, uses field 'id' to identify the record to change in database.

        Args:
            itemData (Item): New item-data

        Raises:
            ItemNotFound: No item with the provided id ('itemData.id') found.

        Returns:
            Item: New version of the item
        """
        try:
            newData = self.DatabaseConnection.updateItem (itemData.dict())
            return Item.parse_obj(newData)
        
        except IDatabaseConnection.ItemNotFound as itemNotFound:
            raise ItemNotFound (str(itemNotFound)) from itemNotFound

    def deleteItem (self, itemId: int):
        """Deletes item with id 'itemId'

        Args:
            itemId (int): id of item to delete

        Raises:
            ItemNotFound: Item does not exist
        """
        try:
            self.DatabaseConnection.deleteItem (itemId)
            
        except IDatabaseConnection.ItemNotFound as itemNotFound:
            raise ItemNotFound (str(itemNotFound)) from itemNotFound


class ItemNotFound (Exception):
    pass