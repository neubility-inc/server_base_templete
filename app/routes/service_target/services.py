import datetime
from sqlalchemy import select

# from sqlalchemy.orm.session import Session
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.params import Depends
from app.routes.service_target import ServiceTargetBaseHandler
from app.database.database import database

# from app.database.models.service_target import ServiceTarget
from app.database.models import ServiceTarget

# from app.routes.service_target.service_target_v1 import ServiceTargetController
from app.database.repository.service_target_repository import ServiceTargetRepository
import asyncio


class ServiceTargetHandler(ServiceTargetBaseHandler):
    @classmethod
    async def get_service_target_by_service_target_id(cls, service_target_id: str):
        return await ServiceTargetRepository(database.session).get_service_target_by_id(
            service_target_id
        )
