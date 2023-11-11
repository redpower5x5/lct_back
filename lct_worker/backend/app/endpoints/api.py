from fastapi import APIRouter

from app.endpoints.auth import router as auth_router
from app.endpoints.cams import router as cams_router
from app.endpoints.files import router as files_router


router = APIRouter(
    prefix="/api",
    responses={404: {"description": "Not found"}},
)

router.include_router(auth_router)
router.include_router(cams_router)
router.include_router(files_router)
