from fastapi_utils.cbv import cbv as class_based_view
from fastapi_utils.inferring_router import InferringRouter
from fastapi import Depends
from app.routes import BaseController
from app.common.logger import logger

t_router = InferringRouter()


@class_based_view(t_router)
class TestController(BaseController):
    def __init__(self):
        super().__init__()

    @t_router.get("/test_code")
    async def tttest(self):
        response = await self._test_handler.get_test_data()
        return self.response(response, "", 200)
