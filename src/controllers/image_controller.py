from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from src.controllers.auth_controller import oauth2_scheme
from src.exceptions import SessionDoesntExistException
from src.services.auth_service import verify_token
from src.services.image_service import create_image

router = APIRouter(tags=["Images"])


@router.post("/sessions/{session_id}/images/")
async def upload_image(session_id: int, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)):

    if not verify_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    try:
        return create_image(session_id, file.filename)
    except SessionDoesntExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
