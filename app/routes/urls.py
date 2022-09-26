from fastapi import APIRouter

from .user_auth.user_auth_v1 import user_auth_router


router = APIRouter()

router.include_router(user_auth_router, prefix="/v1", tags=["auth"])
