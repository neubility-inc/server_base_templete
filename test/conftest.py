import pytest

from app.database.database import DatabaseSession
from uuid import uuid4


@pytest.fixture(scope="function")
def database():
    database = DatabaseSession()

    context = database.set_session_context(str(uuid4()))

    database.create_engine()
    database.create_session()

    return database
