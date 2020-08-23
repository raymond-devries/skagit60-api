from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    active: bool


class UserIn(User):
    hashed_password: str
