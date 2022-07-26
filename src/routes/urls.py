from fastapi import APIRouter

#from .meta.router import meta_router

router = APIRouter()

"""
router.include_router(
    meta_router,
    prefix='/v1/meta',
    tags=['meta']
)
"""