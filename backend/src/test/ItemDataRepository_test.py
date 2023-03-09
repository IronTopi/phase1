import random
import pytest

from pydantic import ValidationError

from dataaccess.ItemDataRepository import ItemDataRepository, ItemNotFound
from test.mocks.MockDatabaseConnection import MockDatabaseConnection
from test.mocks.MockDatabaseConnectionFaultyItems import MockDatabaseConnectionFaultyItems as FaultyDatabase
from test.backend_http_integration_test import buildGoodItemJson

from api.models.Item import Item


@pytest.fixture()
def itemDataRepository() -> ItemDataRepository:
    """Produces an fresh (empty) ItemDataRepository

    Yields:
        ItemDataRepository: empty ItemDataRepository
    """
    dataRepo = ItemDataRepository(MockDatabaseConnection({}))
    yield dataRepo


@pytest.fixture()
def filledRepo(itemDataRepository: ItemDataRepository) -> ItemDataRepository:
    """Produces a filled ItemDataRepository (50 - 100 entries, random)

    Args:
        itemDataRepository (ItemDataRepository): empty ItemDataRepository to be filled

    Yields:
        ItemDataRepository: Pre-filled ItemDataRepository
    """
    for _ in range(50, 100):
        itemDataRepository.insertItem(Item.parse_obj(buildGoodItemJson()))

    yield itemDataRepository


@pytest.fixture
def faultyRepoSetup() -> ItemDataRepository:
    """Produces an ItemDataRepository with a faulty database.
    Returns non-Item-like data for any requested itemId.

    Yields:
        ItemDataRepository: faulty ItemDataRepository
    """
    dataRepo = ItemDataRepository(FaultyDatabase({}))
    yield dataRepo


def test_deleteItem(filledRepo: ItemDataRepository):
    allItems = filledRepo.getAllItems()

    randomItem = random.choice(allItems)
    # Nothing supposed to habben if the delete went through
    filledRepo.deleteItem(randomItem.id)


def test_deleteNonExistingItem(itemDataRepository: ItemDataRepository):
    item = itemDataRepository.insertItem(Item.parse_obj(buildGoodItemJson()))
    wrongItemId = item.id + item.id

    with pytest.raises(ItemNotFound) as info:
        itemDataRepository.deleteItem(wrongItemId)


def test_getAllItems(filledRepo: ItemDataRepository):
    allItems = filledRepo.getAllItems()


def test_getItem(filledRepo: ItemDataRepository):
    allItems = filledRepo.getAllItems()

    randomItem = random.choice(allItems)
    filledRepo.getItem(randomItem.id)


def test_getMissingItem(itemDataRepository: ItemDataRepository):
    item = itemDataRepository.insertItem(Item.parse_obj(buildGoodItemJson()))
    wrongItemId = item.id + item.id

    with pytest.raises(ItemNotFound) as info:
        itemDataRepository.getItem(wrongItemId)


def test_updateMissingItem(itemDataRepository: ItemDataRepository):
    # We start with an empty repo and inserted only one item,
    # so this will give an id that cannot exist in the db

    item = itemDataRepository.insertItem(Item.parse_obj(buildGoodItemJson()))
    wrongItemId = item.id + item.id
    item.id = wrongItemId

    with pytest.raises(ItemNotFound) as info:
        itemDataRepository.updateItem(item)


def test_updateItem(filledRepo: ItemDataRepository):
    allItems = filledRepo.getAllItems()

    randomItem = random.choice(allItems)
    randomItem.city = randomItem.city + " changed"
    # Nothing supposed to habben if the delete went through
    filledRepo.updateItem(randomItem)


############
# Faulty data in database
def test_insertItem_faulty(faultyRepoSetup: ItemDataRepository):
    with pytest.raises(ValidationError) as info:
        faultyRepoSetup.insertItem(Item.parse_obj(buildGoodItemJson()))


def test_getItem_faulty(faultyRepoSetup: ItemDataRepository):
    with pytest.raises(ValidationError) as info:
        faultyRepoSetup.getItem(1)
