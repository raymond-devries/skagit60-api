from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import security
from app.database.database_utils import get_db
from app.models import user_model

router = APIRouter()


@router.get("/user/profile/", response_model=user_model.User)
async def get_profile(
    current_user: user_model.UserInDb = Depends(security.get_current_user),
):
    return current_user


@router.post("/signup/", status_code=status.HTTP_201_CREATED)
async def create_user(user: user_model.UserSignUp, db=Depends(get_db)):
    user = user_model.UserBeforeDb(active=True, **user.dict())
    await security.create_user_and_hash_password(user, db)


@router.post("/token/", response_model=user_model.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)
):
    user = await security.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_user_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}
