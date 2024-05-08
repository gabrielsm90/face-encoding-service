from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from src.controllers.auth_controller import oauth2_scheme
from src.exceptions import SessionDoesntExistException, MaxNumberOfImagesException
from src.schemas.image import Image
from src.services.auth_service import verify_token
from src.services.image_service import create_image

router = APIRouter(tags=["Images"])


@router.post("/sessions/{session_id}/images/")
async def upload_image(session_id: int, file: UploadFile = File(...), token: str = Depends(oauth2_scheme)) -> Image:

    if not verify_token(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")

    try:
        file_content = await file.read()
        image = create_image(session_id, file.filename, file_content)
        return image
    except SessionDoesntExistException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    except MaxNumberOfImagesException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
