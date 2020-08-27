from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException
from jose import jwt
from tests.factories import user_factories

from app import security, settings
from app.database import users_db


@pytest.mark.asyncio
async def test_authenticate_user_correct_password(fake_db):
    test_password = "testing123"
    hashed_password = security.crypt.hash(test_password)
    user = user_factories.UserInFactory(hashed_password=hashed_password)
    await users_db.create_user_db(user, fake_db)
    assert (
        await security.authenticate_user(user.username, test_password, fake_db) == user
    )


@pytest.mark.asyncio
async def test_authenticate_user_user_not_active(fake_db):
    test_password = "testing123"
    hashed_password = security.crypt.hash(test_password)
    user = user_factories.UserInFactory(hashed_password=hashed_password, active=False)
    await users_db.create_user_db(user, fake_db)
    assert (
        await security.authenticate_user(user.username, test_password, fake_db) is False
    )


@pytest.mark.asyncio
async def test_authenticate_user_wrong_password(fake_db):
    hashed_password = security.crypt.hash("testing312")
    user = user_factories.UserInFactory(hashed_password=hashed_password)
    await users_db.create_user_db(user, fake_db)
    assert (
        await security.authenticate_user(user.username, "password", fake_db,) is False
    )


@pytest.mark.asyncio
async def test_authenticate_user_that_doesnt_exist(fake_db):
    assert await security.authenticate_user("user", "password", fake_db,) is False


@pytest.mark.asyncio
async def test_get_current_user_valid_user(fake_db):
    username = "user1"
    user = user_factories.UserInFactory(username=username)
    await users_db.create_user_db(user, fake_db)
    token = security.create_user_access_token(username)
    assert await security.get_current_user(token=token, db=fake_db) == user


@pytest.mark.asyncio
async def test_get_current_user_invalid_user(fake_db):
    token = security.create_user_access_token("user2")
    with pytest.raises(HTTPException):
        await security.get_current_user(token=token, db=fake_db)


@pytest.mark.asyncio
async def test_get_current_active_user_expired_token(fake_db):
    username = "user3"
    user = user_factories.UserInFactory(username=username)
    await users_db.create_user_db(user, fake_db)
    token = jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) - timedelta(days=3)},
        settings.SECRET_KEY,
    )
    with pytest.raises(HTTPException):
        await security.get_current_user(token=token, db=fake_db)


def test_create_access_token():
    username = "user1"
    token = security.create_user_access_token(username)
    decoded = jwt.decode(token, settings.SECRET_KEY)
    assert decoded["sub"] == username


@pytest.mark.asyncio
async def test_create_user_and_hash_password(fake_db):
    user_before = user_factories.UserBeforeFactory()
    await security.create_user_and_hash_password(user_before, fake_db)
    created_user = await users_db.get_user_db(user_before.username, fake_db)
    assert "unhashed_password" not in created_user
    assert user_before.unhashed_password not in created_user.values()
    assert security.crypt.verify(
        user_before.unhashed_password, created_user["hashed_password"]
    )
