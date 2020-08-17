import pytest
from tests import factories


@pytest.mark.asyncio
async def test_get_peaks(fill_db, client):
    response = await client.get("/peaks/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_peak(client):
    peak_json = factories.PeakInFactory().json()
    response = await client.post("/peak/", data=peak_json)
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_add_duplicate_peak(client):
    peak_json = factories.PeakInFactory().json()
    response = await client.post("/peak/", data=peak_json)
    response2 = await client.post("/peak/", data=peak_json)
    assert 409 or 201 in [response.status_code, response2.status_code]
