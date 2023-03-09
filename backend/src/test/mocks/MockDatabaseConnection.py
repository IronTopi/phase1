from typing import Dict, Any, List

from dataaccess.IDatabaseConnection import IDatabaseConnection, ItemNotFound


class MockDatabaseConnection(IDatabaseConnection):
    def __init__(self, connectionData: Dict[str, Any]):
        self.Data: Dict[int, Any] = {}
        self.IdCounter = 0

    def convertToNotFound(func: callable):
        # Converts KeyError into domain-specific ItemNotFound error.
        # Maaaaan it might have been smart to use the KeyError in our design...
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)

            except KeyError as ke:
                raise ItemNotFound from ke

        return wrapper

    def getAllItems(self) -> List[Dict]:
        return self.Data.values()

    @convertToNotFound
    def getItem(self, itemId: int) -> Dict:
        return self.Data[itemId]

    def insertItem(self, itemData: Dict) -> Dict:
        self.IdCounter += 1

        itemData["id"] = self.IdCounter
        self.Data[itemData["id"]] = itemData

        return self.Data[itemData["id"]]

    @convertToNotFound
    def updateItem(self, itemData: Dict) -> Dict:
        # Check if item does exist
        # Will raise KeyError if no entry found
        self.Data[itemData["id"]]

        self.Data[itemData["id"]] = itemData

        return self.Data[itemData["id"]]

    @convertToNotFound
    def deleteItem(self, itemId: int):
        del self.Data[itemId]
