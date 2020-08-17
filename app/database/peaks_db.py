from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.database_utils import get_collection
from app.models import peak_model
from app.settings import MAX_DB_QUERY

COLLECTION_NAME = "peaks"


async def get_peaks_db(db: AsyncIOMotorDatabase) -> list:
    cursor = get_collection(COLLECTION_NAME, db).find()
    return [peak for peak in await cursor.to_list(MAX_DB_QUERY)]


async def create_peak_db(peak: peak_model.PeakIn, db: AsyncIOMotorDatabase) -> str:
    data = {
        "display_name": peak.display_name,
        "state": peak.state,
        "country": peak.country,
        "elevation": peak.elevation,
    }
    if await get_collection(COLLECTION_NAME, db).find_one(data):
        raise ValueError(f"A peak with data: {data} already exists")
    insert = await get_collection(COLLECTION_NAME, db).insert_one(peak.dict())
    return str(insert.inserted_id)
