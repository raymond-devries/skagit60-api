from app.database.database_utils import get_collection
from app.models import user_model
from app.settings import MAX_DB_QUERY

COLLECTION_NAME = "users"


async def create_user_indexes(db):
    collection = get_collection(COLLECTION_NAME, db)
    await collection.create_index("username", unique=True)
    await collection.create_index("email", unique=True)


async def create_user_db(user: user_model.UserIn, db):
    await get_collection(COLLECTION_NAME, db).insert_one(user.dict())
