import pytest
from pymongo.errors import DuplicateKeyError
from tests.factories import peak_factories

from app.database import peaks_db
from app.database.database_utils import get_collection
from app.models import peak_model


@pytest.mark.asyncio
async def test_create_peaks(fake_db):
    fake_peak = peak_factories.PeakInFactory()
    expected_peak = peak_model.PeakWithSlug(**fake_peak.dict())
    await peaks_db.create_peak_db(fake_peak, fake_db)
    created_peak = await get_collection(peaks_db.COLLECTION_NAME, fake_db).find_one(
        {"slug": expected_peak.slug}
    )
    assert peak_model.PeakWithSlug(**created_peak) == peak_model.PeakWithSlug(
        **fake_peak.dict()
    )


@pytest.mark.asyncio
async def test_create_duplicate_peaks(fake_db, client):
    fake_peak = peak_factories.PeakInFactory()
    with pytest.raises(DuplicateKeyError):
        await peaks_db.create_peak_db(fake_peak, fake_db)
        await peaks_db.create_peak_db(fake_peak, fake_db)


@pytest.mark.asyncio
async def test_get_peaks(fake_db):
    inserts = [
        fake_peak.dict()
        for fake_peak in peak_factories.PeakInFactory.create_batch(size=10)
    ]
    await get_collection(peaks_db.COLLECTION_NAME, fake_db).insert_many(inserts)
    results = await peaks_db.get_peaks_db(fake_db)
    assert results == inserts
