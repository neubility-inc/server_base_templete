from starlette.types import Receive, Scope, Send
from datetime import datetime, timedelta
from typing import List
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Receive, Scope, Send
from uuid import uuid4
from app.database.database import database


class SQLAlchemyMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        session_id = str(uuid4())
        context = database.set_session_context(session_id=session_id)
        try:
            await self.app(scope, receive, send)
        except Exception as e:
            raise e
        finally:
            await database.session.remove()
            await database.session.close()
            database.reset_session_context(context=context)
