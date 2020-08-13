from motor.core import AgnosticCollection
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.settings import DB_NAME


async def get_db():
    return AsyncIOMotorClient()[DB_NAME]


def get_collection(name: str, db: AsyncIOMotorDatabase) -> AgnosticCollection:
    return db[name]


def clean_results(results: list) -> list:
    for result in results:
        result["_id"] = str(result["_id"])

    return results
