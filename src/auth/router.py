from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta

from src.database.repositories import UserRepository
from src.config import ACCESS_TOKEN_EXPIRE_HOURS
from src.auth.utils import (
    CURRENT_PREFIX,
    authenticate_user,
    create_access_token,
    get_password_hash
)

router = APIRouter(prefix=f"/{CURRENT_PREFIX}")


@router.post("/token")
async def token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Returns the authorization token for the registered user
    """
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/new")
async def new_account(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Creates a new account if a user with a similar username does not already exist
    """
    user_rep = UserRepository(form_data.username)
    user = await user_rep.get()

    if user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account already exists",
        )
    
    password_hash = get_password_hash(form_data.password)
    await user_rep.new(password_hash)

    return {
        "message": f"user {form_data.username} was created"
    }
    