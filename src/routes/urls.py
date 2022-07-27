from fastapi import APIRouter

from .neubility_api_access_key.neubility_api_access_v1 import neubility_api_access_key_v1_router

router = APIRouter()


router.include_router(
    neubility_api_access_key_v1_router,
    prefix='/v1/access_key',
    tags=['access','key']
)
