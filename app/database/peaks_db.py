from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.database_utils import get_collection
from app.models import peak_model
from app.settings import MAX_DB_QUERY

COLLECTION_NAME = "peaks"


async def get_peaks_db(db: AsyncIOMotorDatabase) -> list:
    cursor = get_collection(COLLECTION_NAME, db).find()
    return [peak for peak in await cursor.to_list(MAX_DB_QUERY)]


async def create_peak_db(peak: peak_model.Peak, db: AsyncIOMotorDatabase) -> str:
    insert = await get_collection(COLLECTION_NAME, db).insert_one(peak.dict())
    return str(insert.inserted_id)
