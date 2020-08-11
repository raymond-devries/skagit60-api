from app.database import database_utils
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection


def test_get_client():
    assert isinstance(database_utils.get_client(), AsyncIOMotorClient)


def test_get_db():
    assert isinstance(database_utils.get_db('tests'), AsyncIOMotorDatabase)


def test_get_collection():
    assert isinstance(database_utils.get_collection('test'), AsyncIOMotorCollection)
