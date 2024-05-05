from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src.exceptions import UserAlreadyExists
from src.services.auth_service import login, register_user

router = APIRouter(tags=["Authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post("/auth/token")
def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    access_token = login(form_data.username, form_data.password)

    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/auth/register")
def register_new_user(form_data: OAuth2PasswordRequestForm = Depends()) -> dict[str, str]:
    try:
        register_user(form_data.username, form_data.password)
    except UserAlreadyExists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    return {"message": "User registered successfully"}
