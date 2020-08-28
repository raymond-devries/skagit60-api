from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.database.database_utils import get_db
from app.database.users_db import create_user_db, get_user_db
from app.models import user_model
from app.models.user_model import UserInDb
from app.settings import SECRET_KEY

crypt = CryptContext(["argon2", "django_pbkdf2_sha256"], default="argon2")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def authenticate_user(username_or_email, password, db):
    user = await get_user_db(username_or_email, db)
    if user is None:
        return False
    user = UserInDb(**user)
    if not user.active:
        return False
    if crypt.verify(password, user.hashed_password):
        return user
    return False


async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
        username: str = payload.get("sub")
        token_data = user_model.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_db(token_data.username, db)
    if user is None:
        raise credentials_exception
    user = UserInDb(**user)
    return user


def create_user_access_token(username: str):
    return jwt.encode(
        {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(days=3)},
        SECRET_KEY,
    )


async def create_user_and_hash_password(user: user_model.UserBeforeDb, db):
    hashed_password = crypt.hash(user.unhashed_password)
    user = user_model.UserInDb(hashed_password=hashed_password, **user.dict())
    await create_user_db(user, db)
