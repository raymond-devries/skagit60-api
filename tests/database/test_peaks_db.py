import pytest
from bson.objectid import ObjectId
from tests import factories

from app.database import peaks_db
from app.database.database_utils import get_collection


@pytest.mark.asyncio
async def test_create_peaks(fake_db):
    fake_peak = factories.PeakInFactory()
    result = await peaks_db.create_peak_db(fake_peak, fake_db)
    created_peak = await get_collection(peaks_db.COLLECTION_NAME, fake_db).find_one(
        ObjectId(result)
    )
    expected_result = {**{"_id": ObjectId(result)}, **fake_peak.dict()}
    assert created_peak == expected_result


@pytest.mark.asyncio
async def test_get_peaks(fake_db):
    inserts = [
        fake_peak.dict() for fake_peak in factories.PeakInFactory.create_batch(size=10)
    ]
    await get_collection(peaks_db.COLLECTION_NAME, fake_db).insert_many(inserts)
    results = await peaks_db.get_peaks_db(fake_db)
    assert results == inserts
