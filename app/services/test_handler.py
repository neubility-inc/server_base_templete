from . import BaseHandler
from app.database.database import transactional


class TestHandler(BaseHandler):
    def __init__(self):
        super().__init__()

    # @transactional
    async def get_test_data(self):
        # self._test_repository. ## 구현필요
        return "test"
