from test.unit.base import TestBase
from aiounittest import async_test
from app.schema.database import CourseCreate, CourseUpdate
from app.database.repository.course_repository import CourseRepository
from app.database import models
from sqlalchemy import select


class TestCourseRepository(TestBase):
    @async_test
    async def test_create_course(self):
        await self.database.create_tables()

        session = self.database.session

        course_name = "세라 코스"
        hole_name = "hole_1"
        point = f"POINT({37.547824} {127.044134})"
        service_target_id = "KM_YEOJU_01"

        await self.create_service_target(session, service_target_id)

        course = CourseRepository(session).create(
            CourseCreate(
                course_name=course_name,
                hole_name=hole_name,
                point=point,
                service_target_id=service_target_id,
            )
        )

        await session.commit()
        await session.flush()

        course = await self.get_course(session)

        self.assertEqual(course.course_name, course_name)
        self.assertEqual(course.hole_name, hole_name)

        await session.close()

        await self.database.drop_tables()

    @async_test
    async def test_update_course(self):
        await self.database.create_tables()

        session = self.database.session

        course = await self.create_course(session)

        hole_name = "hole_123123123"

        course = CourseRepository(session).save(
            course, CourseUpdate(hole_name=hole_name)
        )

        await session.commit()

        self.assertEqual(course.hole_name, hole_name)

        await session.close()

        await self.database.drop_tables()

    async def create_service_target(self, session, service_target_id):

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
        await session.flush()

    async def create_course(self, session):
        course_name = "세라 코스"
        hole_name = "hole_1"
        point = f"POINT({37.547824} {127.044134})"
        service_target_id = "KM_YEOJU_01"

        await self.create_service_target(session, service_target_id)

        course = CourseRepository(session).create(
            CourseCreate(
                course_name=course_name,
                hole_name=hole_name,
                point=point,
                service_target_id=service_target_id,
            )
        )

        await session.commit()

        return course

    async def get_course(self, session) -> models.Course:
        return (await session.execute(select(models.Course))).scalars().one()
