import pytest
from bson.objectid import ObjectId

from app.database import peaks
from app.database.database_utils import get_collection
from app.models import peak_model


@pytest.fixture
def fake_peak():
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


@pytest.mark.asyncio
async def test_create_peaks(fake_peak, fake_db):
    result = await peaks.create_peak(fake_peak, fake_db)
    created_peak = await get_collection(peaks.COLLECTION, fake_db).find_one(
        ObjectId(result)
    )
    expected_result = {**{"_id": ObjectId(result)}, **fake_peak.dict()}
    assert created_peak == expected_result


@pytest.mark.asyncio
async def test_get_peaks(fake_peak, fake_db):
    inserts = [fake_peak.dict() for _ in range(5)]
    await get_collection(peaks.COLLECTION, fake_db).insert_many(inserts)
    results = await peaks.get_peaks(fake_db)
    assert results == inserts
