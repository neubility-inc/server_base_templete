from http.client import BAD_REQUEST
from app.common.exception.db_exception import *
from app.repository import *
from app.database.database import database
from app.repository import *
from uuid import uuid4
from app.common.logger import logger


class BaseHandler:
    def __init__(self):
        # self._test_repository = TestRespository(database.session)

        self._logger = logger
