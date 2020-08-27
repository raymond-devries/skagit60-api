import json

import pytest
from tests.factories import peak_factories

from app.database import peaks_db
from app.models import peak_model


@pytest.mark.asyncio
async def test_get_peaks(client, fake_db):
    inserts = [
        fake_peak.dict()
        for fake_peak in peak_factories.PeakWithSlugFactory.create_batch(60)
    ]
    await fake_db[peaks_db.COLLECTION_NAME].insert_many(inserts)
    response = await client.get("/peaks/")
    peaks_data = [
        json.loads(peak_model.PeakWithSlug(**data).json())
        for data in await peaks_db.get_peaks_db(fake_db)
    ]
    assert response.status_code == 200
    assert response.json() == peaks_data


@pytest.mark.asyncio
async def test_add_peak(client, fake_db):
    peak = peak_factories.PeakInFactory()
    response = await client.post("/peak/", data=peak.json())
    peak = peak_model.PeakWithSlug(**peak.dict())
    assert response.status_code == 201
    peak_in_db = await peaks_db.get_peaks_db(fake_db)
    assert peak_model.PeakWithSlug(**peak_in_db[0]) == peak


@pytest.mark.asyncio
async def test_add_duplicate_peak(client):
    peak_json = peak_factories.PeakInFactory().json()
    response = await client.post("/peak/", data=peak_json)
    response2 = await client.post("/peak/", data=peak_json)
    assert 409 in [response.status_code, response2.status_code]
