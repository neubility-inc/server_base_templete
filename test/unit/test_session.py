import unittest
import asyncio

from uuid import uuid4
from app.database.database import DatabaseSession
from app.utils.session_context import set_session_context
from aiounittest import async_test
from app.database.models.neubility_api_access_key_model import (
    NeubilityApiAccessKeyModel,
)
from sqlalchemy import select


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
    async def test_create_item(self):
        user_id = "cheolhyeon kim"
        value = "12341234123141231231231231231231231"
        token_type = "test"

        await self.database.create_tables()
        session = self.database.session

        session.add(
            NeubilityApiAccessKeyModel(
                user_id=user_id,
                value=value,
                token_type=token_type,
            )
        )

        await session.commit()

        access_key_model = await session.get(NeubilityApiAccessKeyModel, user_id)

        self.assertEqual(access_key_model.user_id, user_id)
        self.assertEqual(access_key_model.value, value)

        # 테스트 데이터 삭제
        await session.delete(access_key_model)
        await session.commit()

        await session.remove()

    @async_test
    async def test_create_test(self):
        await self.database.create_tables()

        user_id = "neubie"
        value = "12341234123141231231231231231231231"
        token_type = "test"

        session = self.database.session

        access_key_model = NeubilityApiAccessKeyModel(
            user_id=user_id,
            value=value,
            token_type=token_type,
        )

        session.add(access_key_model)
        await session.commit()

        self.assertEqual(access_key_model.user_id, user_id)
        self.assertEqual(access_key_model.value, value)

        # 테스트 데이터 삭제
        await session.delete(access_key_model)
        await session.commit()

        await session.remove()
