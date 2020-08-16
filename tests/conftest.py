import pytest
from motor.motor_asyncio import AsyncIOMotorClient
from tests import factories

from app.database import peaks_db
from app.database.database_utils import get_db
from app.main import app
from app.settings import DB_SERVER, TEST_DB_NAME


@pytest.yield_fixture
async def fake_db():
    client = AsyncIOMotorClient(DB_SERVER)
    db = client[TEST_DB_NAME]
    yield db
    client.drop_database(TEST_DB_NAME)


async def create_fake_db():
    client = AsyncIOMotorClient(DB_SERVER)
    db = client[TEST_DB_NAME]
    yield db
    client.drop_database(TEST_DB_NAME)


@pytest.fixture(autouse=True)
def override_db():
    app.dependency_overrides[get_db] = create_fake_db


@pytest.fixture
async def fill_db(fake_db):
    inserts = [fake_peak.dict() for fake_peak in factories.PeakFactory.create_batch(60)]
    await fake_db[peaks_db.COLLECTION_NAME].insert_many(inserts)
