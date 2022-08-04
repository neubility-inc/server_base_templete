import unittest
import asyncio

from uuid import uuid4
from app.database.database import DatabaseSession
from app.utils.session_context import set_session_context
from aiounittest import async_test
from sqlalchemy import select
from app.database import models


class TestSession(unittest.TestCase):
    def setUp(self) -> None:
        self.session_id = str(uuid4())
        self.context = set_session_context(self.session_id)

        """
            DB 세션 객체는 이벤트 루프 당 하나를 생성해야 한다.
            async_test 데코레이터는 각 테스트 케이스 마다 이벤트 루프를 생성하므로
            각 테스트 케이스를 실행하기 전에 실행되는 setUp 함수에서 세션 객체를 생성한다
        """
        self.database = DatabaseSession()
        self.database.create_database_session()

    @async_test
    async def test_create_service_target(self):
        service_target_id = "KM_YEOJU_02"
        description = "카모 서비스"
        service_target_name = "여주 세라지오"

        await self.database.create_tables()
        session = self.database.session

        session.add(
            models.ServiceTarget(
                service_target_id=service_target_id,
                service_target_name=service_target_name,
                description=description,
            )
        )

        await session.commit()

        service_target = await session.get(models.ServiceTarget, service_target_id)

        self.assertEqual(service_target.service_target_id, service_target_id)
        self.assertEqual(service_target.service_target_name, service_target_name)

        # 테스트 데이터 삭제
        await session.delete(service_target)
        await session.commit()

        await session.remove()

    @async_test
    async def test_create_course(self):
        course_name = "세라 코스"
        hole_name = "hole_1"
        point = f"POINT({37.4021} {127.1086})"
        service_target_id = "KM_YEOJU_01"

        await self.database.create_tables()
        session = self.database.session

        await self.create_service_target(session)

        course = models.Course(
            course_name=course_name,
            hole_name=hole_name,
            point=point,
            service_target_id=service_target_id,
        )

        session.add(course)

        await session.commit()
        await session.refresh(course)

        query = await session.execute(
            select(models.Course).where(models.Course.id == course.id)
        )
        course_db = query.scalars().first()

        self.assertEqual(course_db.course_name, course_name)
        self.assertEqual(course_db.hole_name, hole_name)

        from app.utils.geometry import parse_point_to_xy

        x, y = parse_point_to_xy(course.point)
        self.assertEqual(x, 37.4021)
        self.assertEqual(y, 127.1086)

        # 테스트 데이터 삭제
        await session.delete(course)
        await session.commit()

        service_target = await session.get(models.ServiceTarget, service_target_id)
        await session.delete(service_target)
        await session.commit()

        await session.remove()

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
