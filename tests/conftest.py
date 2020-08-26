import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from tests.factories import peak_factories

from app import main
from app.database import peaks_db
from app.database.database_utils import get_db
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
    return db


@pytest.yield_fixture(autouse=True)
def override_db():
    main.app.dependency_overrides[get_db] = create_fake_db
    yield
    client = AsyncIOMotorClient(DB_SERVER)
    client.drop_database(TEST_DB_NAME)


@pytest.yield_fixture
async def client(fake_db):
    [await main.start_up_tasks(db=fake_db) for _ in range(2)]
    async with AsyncClient(app=main.app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def fill_db(fake_db):
    inserts = [
        fake_peak.dict() for fake_peak in peak_factories.PeakOutFactory.create_batch(60)
    ]
    await fake_db[peaks_db.COLLECTION_NAME].insert_many(inserts)
