from test.mocks.MockDatabaseConnection import MockDatabaseConnection


class MockDatabaseConnectionFaultyItems(MockDatabaseConnection):
    """Only returns gibberish that cannot be parsed back into an item.

    Args:
        MockDatabaseConnection (IDatabaseConnection): Properly working implementation that we can rig
    """

    def __init__(self, connectionData: Dict[str, Any]):
        super().__init__(connectionData)
