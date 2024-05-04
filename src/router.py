from fastapi import APIRouter

from src.controllers.system_controller import router as system_router
from src.controllers.auth_controller import router as auth_router

router = APIRouter()

router.include_router(system_router)
router.include_router(auth_router)
