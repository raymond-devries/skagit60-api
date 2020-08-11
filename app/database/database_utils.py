from motor.motor_asyncio import AsyncIOMotorClient
from motor.core import AgnosticCollection

DB_NAME = "skagit60"


def get_client():
    return AsyncIOMotorClient()


def get_db(db_name: str):
    return get_client()[db_name]


def get_collection(collection_name: str) -> AgnosticCollection:
    return get_db(DB_NAME)[collection_name]

