from fastapi import APIRouter, Depends, status, HTTPException

from src.controllers.auth_controller import oauth2_scheme
from src.services.auth_service import verify_token
from src.services.session_service import create_session, get_session
from src.schemas.session import Session

router = APIRouter(tags=["Sessions"])


@router.post("/sessions", response_model=Session)
def start_session(token: str = Depends(oauth2_scheme)) -> Session:

    if not verify_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    return create_session()


@router.get("/sessions/{session_id}", response_model=Session)
def get_session_by_id(session_id: int, token: str = Depends(oauth2_scheme)) -> Session:

    if not verify_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    return get_session(session_id)
