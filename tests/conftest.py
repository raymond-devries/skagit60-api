import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app import main
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
