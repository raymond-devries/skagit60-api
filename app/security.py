from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.database.users_db import create_user_db, get_user_db
from app.models import user_model
from app.models.user_model import UserIn
from app.settings import SECRET_KEY

crypt = CryptContext(["argon2", "django_pbkdf2_sha256"], default="argon2")


async def authenticate_user(username_or_email, password, db):
    user = await get_user_db(username_or_email, db)
    if user is None:
        return False
    user = UserIn(**user)
    if not user.active:
        return False
    if crypt.verify(password, user.hashed_password):
        return user
    return False


def create_user_access_token(username: str):
    return jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(days=3)},
        SECRET_KEY,
    )


async def create_user_and_hash_password(user: user_model.UserBefore, db):
    hashed_password = crypt.hash(user.unhashed_password)
    user = user_model.UserIn(hashed_password=hashed_password, **user.dict())
    await create_user_db(user, db)
