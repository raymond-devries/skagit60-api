from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.database.database_utils import get_collection
from app.models import peak_model
from app.settings import MAX_DB_QUERY

COLLECTION = "peaks"


async def create_peak(peak: peak_model.Peak, db: AsyncIOMotorDatabase) -> str:
    insert = await get_collection(COLLECTION, db).insert_one(peak.dict())
    return str(insert.inserted_id)


async def get_peaks(db: AsyncIOMotorDatabase):
    cursor = get_collection(COLLECTION, db).find()
    return [peak for peak in await cursor.to_list(MAX_DB_QUERY)]
