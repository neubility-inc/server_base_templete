from app.services.test_handler import TestHandler


class BaseController:
    def __init__(self):
        self._test_handler = TestHandler()

    @classmethod
    def response(self, response, message, code):
        return {"result": response, "message": message, "code": code}


class BaseHandler:
    pass
