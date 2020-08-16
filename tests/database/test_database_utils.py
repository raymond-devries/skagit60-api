import pytest
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.database import database_utils
from app.settings import DB_NAME


@pytest.mark.asyncio
async def test_get_db():
    assert isinstance(await database_utils.get_db(), AsyncIOMotorDatabase)


@pytest.mark.asyncio
async def test_db_name():
    db = await database_utils.get_db()
    assert db.name == DB_NAME


def test_get_collection(fake_db):
    assert isinstance(
        database_utils.get_collection("test", fake_db), AsyncIOMotorCollection
    )
