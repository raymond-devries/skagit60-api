import pytest
from bson.objectid import ObjectId
from tests.models.test_peak_model import fake_peak

from app.database import peaks
from app.database.database_utils import get_collection


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
