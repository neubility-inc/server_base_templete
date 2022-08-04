from .base_repository import BaseRepository
from sqlalchemy import select
from app.database.models import ServiceTarget
from app.schema.database.service_target import ServiceTargetCreate, ServiceTargetUpdate


class ServiceTargetRepository(
    BaseRepository[ServiceTarget, ServiceTargetCreate, ServiceTargetUpdate]
):
    def __init__(self, session):
        super().__init__(session, ServiceTarget)

    async def delete_service_target(self, service_target_id):
        delete_obj = (
            (
                await self.session.execute(
                    select(ServiceTarget).where(
                        ServiceTarget.service_target_id == service_target_id
                    )
                )
            )
            .scalars()
            .one()
        )

        return await self.delete(delete_obj)

    async def get_service_target_by_id(self, service_target_id):
        return (
            (
                await self.session.execute(
                    select(ServiceTarget).where(
                        ServiceTarget.service_target_id == service_target_id
                    )
                )
            )
            .scalars()
            .one()
        )
