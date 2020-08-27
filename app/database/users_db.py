from app.database.database_utils import get_collection
from app.models import user_model

COLLECTION_NAME = "users"


async def create_user_indexes(db):
    collection = get_collection(COLLECTION_NAME, db)
    await collection.create_index("username", unique=True)
    await collection.create_index("email", unique=True)


async def create_user_db(user: user_model.UserIn, db):
    await get_collection(COLLECTION_NAME, db).insert_one(user.dict())


async def get_user_db(username_or_email: str, db):
    return await get_collection(COLLECTION_NAME, db).find_one(
        {"$or": [{"username": username_or_email}, {"email": username_or_email}]}
    )
