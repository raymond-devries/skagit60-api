import pytest
from httpx import AsyncClient
from tests import factories

from app.main import app


@pytest.mark.asyncio
async def test_get_peaks(fill_db):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/peaks/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_peak():
    peak_json = factories.PeakInFactory().json()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/peak/", data=peak_json)
    assert response.status_code == 200
