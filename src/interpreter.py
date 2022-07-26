import time, json, traceback
from datetime import datetime, timedelta
from typing import List
from fastapi.responses import FileResponse
from starlette.responses import JSONResponse, Response

from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_404_NOT_FOUND,\
    HTTP_401_UNAUTHORIZED, HTTP_429_TOO_MANY_REQUESTS

from starlette.requests import Request
from src.database.models.neubility_api_access_key_model import NeubilityApiAccessKeyModel
from src.database.query.neubility_api_access_key import NeubilityApiAccessKey
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from sqlalchemy.orm.session import Session


class RequestHandlingMiddleware(BaseHTTPMiddleware):
    async def authorize(self, request, database: Session):
        n_key = request.state.query_params.get('nKey')
        if n_key is not None:
            docs: List[NeubilityApiAccessKeyModel] = await NeubilityApiAccessKey.get_api_access_key(api_key=n_key)
            if len(docs) < 1:
                return 401
            doc = docs[0]
            request.state.referer = doc.referer
            if doc.expiry_date is not None:
                now = datetime.now()
                if now > doc.expire_time:
                    return 401
        elif n_key == 'su':
            pass
        return 200
    
    """
    def check_default(self, method, cnt):
        if method == 'GET' and cnt > 2000:
            return False
        elif method == 'POST' and cnt > 1000:
            return False
        elif method == 'PUT' and cnt > 1000:
            return False
        elif method == 'DELETE' and cnt > 1000:
            return False
        return True

    async def set_state(self, request: Request):
        request.state.query_params = dict(request.query_params)
        # request.state.body = json.loads(await request.body())
        request.state.path = request.url.path
        request.state.method = request.method
        # if request.state.method in ['POST', 'PUT']:
        #     request.state.body = await request.json()
        handler_obj = list(filter(lambda el: (el.path_regex.search(request.state.path) != None) and list(el.methods)[0] == request.state.method, self.app.app.routes))
        if len(handler_obj) < 1:
            return False
        request.state.handler = handler_obj[0]
        request.state.quota = {}
        quota = list(filter(lambda el: '@QUOTA:' in el, request.state.handler.tags))
        if len(quota) > 0:
            quota = quota[0]
            quota = quota.replace('@QUOTA:', '')
            temps = quota.split('/')
            request.state.quota['check_count'] = int(temps[0])
            request.state.quota['minutes'] = int(int(temps[1]) / 60)
        return True

    async def _parse_body(self, response):
        body = b""
        async for chunk in response.body_iterator:
            body += chunk
        result = json.loads(body)
        return result
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in ['/docs', '/openapi.json']:
            result = await call_next(request)
            return result
        set_state = await self.set_state(request)
        if not set_state:
            return JSONResponse({"result": None, 'processTime': 0, 'message': 'Not found', 'code': 404},
                         status_code=HTTP_404_NOT_FOUND)
        start_time = time.time()
        response = None
        process_time = None
        try:
            authorize = await self.authorize(request)
            if authorize == 200:
                response = await call_next(request)
            else:
                result, process_time = self._render_4xx_error(authorize, start_time)
                return result
            result = None
            if response.status_code == 200:
                content_type = response.headers.raw[1][1].decode('utf-8')
                if 'application/json' == content_type:
                    content = await self._parse_body(response)
                    content_type = content.get('content_type')
                    if not content_type:
                        result, process_time = self._render_json(response, content, start_time)
                    else:
                        result, process_time = self._render_file(response, content, start_time)
                elif 'text/html' in content_type:
                    result = response
                else:
                    result, process_time = self._render_unkown(content_type, start_time)
            else:
                result, process_time = self._render_4xx_error(response.status_code, start_time)
        except Exception as e:
            error_message = traceback.format_exc()
            print(error_message)
            result, process_time = self._render_5xx_error(response, start_time, error_message)
            #res = await ApiHistoryUtil.logging_api_history(request, process_time, 500, error_message)
            return result

        return result

    def _render_json(self, response, content, start_time):
        process_time = time.time() - start_time
        result = {
            'processTime': process_time,
            'code': content.get('code'),
            'message': content.get('message'),
            'result': content.get('result')
        }

        content = json.dumps(result)
        response.headers.update({'Content-Length': str(len(content))})
        return Response(
            content=content,
            status_code=result.get('code'),
            headers=dict(response.headers),
            media_type=response.media_type
        ), process_time
    
    def _render_file(self, response, content, start_time):
        process_time = time.time() - start_time
        return FileResponse(path=content.get('result').get('path'), filename=content.get('result').get('filename')), process_time

    def _render_unkown(self, content_type, start_time):
        process_time = time.time() - start_time
        content = {
            'message': f'unkown content type type: {content_type}',
            'code': 500,
            'processTime': process_time,
            'result': {}
        }
        return JSONResponse(
            content,
            status_code=HTTP_500_INTERNAL_SERVER_ERROR
        ), process_time

    def _render_4xx_error(self, status_code, start_time):
        process_time = time.time() - start_time
        result = None
        if status_code == 404:
            result = JSONResponse({"result": None, 'processTime': process_time, 'message': 'Not found', 'code': status_code},
                                  status_code=HTTP_404_NOT_FOUND)
        elif status_code == 401:
            result = JSONResponse({"result": None, 'processTime': process_time, 'message': 'Unauthorized', 'code': status_code},
                                  status_code=HTTP_401_UNAUTHORIZED)
        elif status_code == 422:
            result = JSONResponse({"result": None, 'processTime': process_time, 'message': 'Unprocessable Entity', 'code': status_code},
                                status_code=HTTP_422_UNPROCESSABLE_ENTITY)
        elif status_code == 429:
            result = JSONResponse(
                {"result": None, 'processTime': process_time, 'message': 'Too many requests', 'code': status_code},
                status_code=HTTP_429_TOO_MANY_REQUESTS)
        else:
            result = JSONResponse(
                {"result": None, 'processTime': process_time, 'message': '', 'code': status_code},
                status_code=status_code)
        return result, process_time

    def _render_5xx_error(self, response, start_time, error_message):
        process_time = time.time() - start_time
        return JSONResponse({"result": None, 'processTime': process_time, 'message': 'Internal Server Error', 'code': 500},
                                  status_code=HTTP_500_INTERNAL_SERVER_ERROR), process_time
