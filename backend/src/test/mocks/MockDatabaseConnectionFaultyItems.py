from typing import Dict, Any
from collections import UserDict
from test.mocks.MockDatabaseConnection import MockDatabaseConnection


class MockDatabaseConnectionFaultyItems(MockDatabaseConnection):
    """Only returns gibberish that cannot be parsed back into an item.

    Args:
        MockDatabaseConnection (IDatabaseConnection): Properly working implementation that we can rig
    """

    def __init__(self, connectionData: Dict[str, Any]):
        super().__init__(connectionData)

        self.Data = FaultyDict({})


class FaultyDict(UserDict):
    def __getitem__(self, __key) -> Dict:
        return {"asdf": 234.234, "id": 24, "city": 12, "price": "two baananas"}
