from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/")
def index():
    return {"message": "Welcome to Veriff's Face Encoding Service!"}


@router.get("/health")
def health():
    return {"status": "ok"}
