import pytest
from tests.factories import user_factories

from app import security
from app.database import users_db


@pytest.mark.asyncio
async def test_authenticate_user(fake_db):
    test_password = "testing123"
    hashed_password = security.crypt.hash(test_password)
    user = user_factories.UserInFactory(hashed_password=hashed_password)
    await users_db.create_user_db(user, fake_db)
    assert (
        await security.authenticate_user(fake_db, test_password, username=user.username)
        == user
    )


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(fake_db):
    hashed_password = security.crypt.hash("testing312")
    user = user_factories.UserInFactory(hashed_password=hashed_password)
    await users_db.create_user_db(user, fake_db)
    assert (
        await security.authenticate_user(fake_db, "password", username=user.username)
        is False
    )


@pytest.mark.asyncio
async def test_authenticate_user_that_doesnt_exist(fake_db):
    assert await security.authenticate_user(fake_db, "pass", username="person") is False
