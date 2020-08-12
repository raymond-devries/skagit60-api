import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from app.models import peak_model
from app.settings import TEST_DB_NAME


@pytest.yield_fixture
def fake_db():
    client = AsyncIOMotorClient()
    db = client[TEST_DB_NAME]
    yield db
    client.drop_database(TEST_DB_NAME)


@pytest.fixture
def fake_peak() -> peak_model.Peak:
    return peak_model.Peak(
        name="test",
        display_name="testing",
        elevation=1000,
        lat=45.77,
        long=120.68,
        state="WA",
        country="USA",
        peakbagger_link="https://peakbagger.com/test",
    )
