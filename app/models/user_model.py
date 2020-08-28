from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str


class UserSignUp(User):
    unhashed_password: str


class _UserDb(User):
    active: bool
    staff: bool = False
    admin: bool = False


class UserBeforeDb(_UserDb):
    unhashed_password: str


class UserInDb(_UserDb):
    hashed_password: str
