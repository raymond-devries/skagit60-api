import pytest
from tests.factories import user_factories

from app.database import users_db
from app.database.database_utils import get_collection


@pytest.mark.asyncio
async def test_create_user_db(fake_db):
    fake_user = user_factories.UserInDbFactory()
    await users_db.create_user_db(fake_user, fake_db)
    created_user = await get_collection(users_db.COLLECTION_NAME, fake_db).find_one(
        fake_user.dict()
    )
    del created_user["_id"]
    assert created_user == fake_user.dict()


@pytest.mark.parametrize("field", ["username", "email"])
@pytest.mark.asyncio
async def test_get_user_db(fake_db, field):
    fake_user = user_factories.UserInDbFactory()
    await get_collection(users_db.COLLECTION_NAME, fake_db).insert_one(fake_user.dict())
    user = await users_db.get_user_db(getattr(fake_user, field), fake_db)
    del user["_id"]
    assert user == fake_user.dict()


@pytest.mark.asyncio
async def test_get_user_db_none(fake_db):
    assert await users_db.get_user_db("", fake_db) is None
