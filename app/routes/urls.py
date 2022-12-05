from fastapi import APIRouter

from .test_v1 import t_router

router = APIRouter()

router.include_router(t_router, prefix="/v1", tags=["test"])
