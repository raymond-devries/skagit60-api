import pytest
from tests.factories import user_factories

from app.database import users_db
from app.database.database_utils import get_collection


@pytest.mark.asyncio
async def test_create_user(fake_db):
    fake_user = user_factories.UserInFactory()
    await users_db.create_user_db(fake_user, fake_db)
    created_user = await get_collection(users_db.COLLECTION_NAME, fake_db).find_one(
        fake_user.dict()
    )
    del created_user["_id"]
    assert created_user == fake_user.dict()
