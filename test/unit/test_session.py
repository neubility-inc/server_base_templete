import unittest
import asyncio

from uuid import uuid4
from app.database.database import DatabaseSession
from app.utils.session_context import set_session_context
from aiounittest import async_test


class TestSession(unittest.TestCase):
    def setUp(self) -> None:
        self.session_id = str(uuid4())
        self.context = set_session_context(self.session_id)

    @async_test
    async def test_create_item(self):

        session = DatabaseSession().session

        await asyncio.gather(self.insert_1(session), self.insert_2(session))

        await session.commit()
        await session.remove()
        await session.close()
