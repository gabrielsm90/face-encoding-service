from fastapi import APIRouter

router = APIRouter(tags=["System"])


@router.get("/")
def index() -> dict[str, str]:
    return {"message": "Welcome to Veriff's Face Encoding Service!"}


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
