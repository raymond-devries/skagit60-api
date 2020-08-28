import pytest
from tests.factories import user_factories

from app import security
from app.database import users_db
from app.models import user_model


@pytest.fixture
async def user_and_headers(client, fake_db):
    user = user_factories.UserBeforeDbFactory()
    await security.create_user_and_hash_password(user, fake_db)
    token_response = await client.post(
        "/token/", data={"username": user.username, "password": user.unhashed_password}
    )
    token = token_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    return user, headers


@pytest.mark.asyncio
async def test_get_profile(client, user_and_headers):
    user, headers = user_and_headers
    response = await client.get("/user/profile/", headers=headers)
    assert response.status_code == 200
    assert response.json() == user_model.User(**user.dict())


@pytest.mark.asyncio
async def test_create_user(client, fake_db):
    user = user_factories.UserSignUpFactory()
    response = await client.post("/signup/", json=user.dict())
    assert response.status_code == 201
    user_in_db = await users_db.get_user_db(user.username, fake_db)
    assert (
        user_model.UserSignUp(unhashed_password=user.unhashed_password, **user_in_db)
        == user
    )


@pytest.mark.asyncio
async def test_login_for_access_token_invalid_login(client):
    response = await client.post(
        "/token/", data={"username": "user", "password": "pass"}
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_login_for_access_token_valid_login(client, fake_db):
    user = user_factories.UserBeforeDbFactory()
    await security.create_user_and_hash_password(user, fake_db)
    response = await client.post(
        "/token/", data={"username": user.username, "password": user.unhashed_password}
    )
    assert response.status_code == 200
    access_token = security.create_user_access_token(user.username)
    assert response.json() == {"access_token": access_token, "token_type": "bearer"}
