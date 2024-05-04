from typing import Dict

from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/")
def index() -> Dict[str, str]:
    return {"message": "Welcome to Veriff's Face Encoding Service!"}


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}
