import pymongo

from app.database.database_utils import get_collection
from app.models import peak_model
from app.settings import MAX_DB_QUERY

COLLECTION_NAME = "peaks"


async def create_peak_index(db):
    collection = get_collection(COLLECTION_NAME, db)
    await collection.create_index(
        [
            ("display_name", pymongo.DESCENDING),
            ("state", pymongo.DESCENDING),
            ("country", pymongo.DESCENDING),
            ("elevation", pymongo.DESCENDING),
        ],
        unique=True,
    )


async def get_peaks_db(db) -> list:
    cursor = get_collection(COLLECTION_NAME, db).find()
    return [peak for peak in await cursor.to_list(MAX_DB_QUERY)]


async def create_peak_db(peak: peak_model.PeakIn, db):
    peak = peak_model.PeakWithSlug(**peak.dict())
    await get_collection(COLLECTION_NAME, db).insert_one(peak.dict())
