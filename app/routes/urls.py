from fastapi import APIRouter

from .service_target.service_target_v1 import service_target_v1_router

router = APIRouter()


router.include_router(
    service_target_v1_router, prefix="/v1/service-target", tags=["access"]
)
