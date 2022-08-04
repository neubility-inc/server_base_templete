import unittest

from app.schema.database import ServiceTargetCreate, ServiceTargetUpdate
from aiounittest import async_test
from app.database.repository.service_target_repository import ServiceTargetRepository
from app.database import models
from sqlalchemy import select
from test.unit.base import TestBase


class TestServiceTargetRepository(TestBase):
    @async_test
    async def test_create_service_target(self):
        service_target_id = "KM_YEOJU_02"
        description = "카모 서비스"
        service_target_name = "여주 세라지오"

        await self.database.create_tables()

        session = self.database.session

        service_target = ServiceTargetRepository(session).create(
            ServiceTargetCreate(
                service_target_id=service_target_id,
                service_target_name=service_target_name,
                description=description,
            )
        )

        await session.commit()
        await session.flush()

        service_target = await session.get(models.ServiceTarget, service_target_id)

        self.assertEqual(service_target.service_target_id, service_target_id)
        self.assertEqual(service_target.service_target_name, service_target_name)

        await session.remove()
        await session.close()

        await self.database.drop_tables()

    @async_test
    async def test_delete_service_target(self):
        await self.database.create_tables()

        session = self.database.session

        await self.create_service_target(session)

        service_target_id = "KM_YEOJU_01"

        service_target = await ServiceTargetRepository(session).delete_service_target(
            service_target_id
        )

        await session.commit()

        service_target = await session.get(models.ServiceTarget, service_target_id)

        self.assertIsNone(service_target)

        await session.remove()
        await session.close()

        await self.database.drop_tables()

    @async_test
    async def test_update_service_target(self):
        await self.database.create_tables()

        session = self.database.session

        await self.create_service_target(session)

        service_target_id = "KM_YEOJU_01"
        service_target_name = "카모 테스트 1"

        update_obj = await session.get(models.ServiceTarget, service_target_id)

        service_target = ServiceTargetRepository(session).save(
            update_obj, ServiceTargetUpdate(service_target_name=service_target_name)
        )

        await session.commit()
        await session.flush()

        service_target = await self.get_serivce_target(session, service_target_id)

        self.assertEqual(service_target.service_target_name, service_target_name)

        await session.remove()
        await session.close()

        await self.database.drop_tables()

    async def create_service_target(self, session):
        service_target_id = "KM_YEOJU_01"
        description = "카모 서비스"
        service_target_name = "여주 세라지오"

        session.add(
            models.ServiceTarget(
                service_target_id=service_target_id,
                service_target_name=service_target_name,
                description=description,
            )
        )

        await session.commit()

    async def get_serivce_target(
        self, session, service_target_id
    ) -> models.ServiceTarget:
        return (
            (
                await session.execute(
                    select(models.ServiceTarget).where(
                        models.ServiceTarget.service_target_id == service_target_id
                    )
                )
            )
            .scalars()
            .one()
        )
