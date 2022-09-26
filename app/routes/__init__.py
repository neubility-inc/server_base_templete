import copy


class BaseController:
    def __init__(self):
        pass

    @classmethod
    def response(self, response, message, code):
        return {"result": response, "message": message, "code": code}

    @classmethod
    def parse_query_params(self, request):
        result = {}
        if str(request.query_params) == "":
            return result
        parameter = str(request.query_params).split("&")
        for param in parameter:
            p = param.split("=")
            result[p[0]] = p[1]
        return result


class BaseHandler:
    def __init__(self):
        pass

    def make_default_dict(self, data_set, dataType):
        return {x: copy.deepcopy(dataType) for x in data_set}
