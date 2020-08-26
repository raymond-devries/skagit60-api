from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.database.users_db import get_user_db
from app.models.user_model import UserIn
from app.settings import SECRET_KEY

crypt = CryptContext(["argon2", "django_pbkdf2_sha256"], default="argon2")


async def authenticate_user(db, password, username="", email=""):
    user = await get_user_db(db, username=username, email=email)
    if user is None:
        return False
    user = UserIn(**user)
    if crypt.verify(password, user.hashed_password):
        return user
    return False


def create_user_access_token(user_id: str):
    return jwt.encode(
        {"sub": user_id, "exp": datetime.now(timezone.utc) + timedelta(days=3)},
        SECRET_KEY,
    )
