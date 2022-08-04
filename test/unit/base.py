import unittest

from uuid import uuid4
from app.database.database import DatabaseSession
from app.utils.session_context import set_session_context


class TestBase(unittest.TestCase):
    def setUp(self) -> None:
        self.session_id = str(uuid4())
        self.context = set_session_context(self.session_id)

        self.database = DatabaseSession()
        self.database.create_database_session()
