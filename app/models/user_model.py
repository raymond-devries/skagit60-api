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
    active: bool


class UserBefore(User):
    unhashed_password: str


class UserIn(User):
    hashed_password: str
