import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from app.settings import TEST_DB_NAME


@pytest.yield_fixture
def fake_db():
    client = AsyncIOMotorClient()
    db = client[TEST_DB_NAME]
    yield db
    client.drop_database(TEST_DB_NAME)
