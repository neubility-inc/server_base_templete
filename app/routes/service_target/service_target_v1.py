from app.routes.service_target import ServiceTargetBaseController
from app.routes.service_target.services import ServiceTargetHandler

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends
from app.database.database import database

# from fastapi.params import Depends
# from app.database.database import database
# from sqlalchemy.orm.session import Session
import asyncio

service_target_v1_router = InferringRouter()


@cbv(service_target_v1_router)
class ServiceTargetController(ServiceTargetBaseController):
    @service_target_v1_router.get("/test", tags=["service-target"])
    async def service_target_info(self, service_target_id):

        response = await ServiceTargetHandler.get_service_target_by_service_target_id(
            service_target_id
        )

        return {
            "result": response,
            "message": "",
            "code": 200,
        }
