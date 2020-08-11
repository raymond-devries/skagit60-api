from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.database import database_utils
from app.settings import DB_NAME


def test_get_db():
    assert isinstance(database_utils.get_db(), AsyncIOMotorDatabase)


def test_db_name():
    assert database_utils.get_db().name == DB_NAME


def test_get_collection(fake_db):
    assert isinstance(
        database_utils.get_collection("test", fake_db), AsyncIOMotorCollection
    )
