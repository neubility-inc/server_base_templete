from dataclasses import asdict
from fastapi.applications import FastAPI
from starlette.responses import Response
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from .common.error import http_422_error_handler, http_error_handler
from .common.custom_route import CustomRoute
from .routes.urls import router as api_router
from datetime import datetime, timedelta
from pydantic import BaseSettings

# from .routes.urls import base_router as base_router
from app.routes.base import base_router
from .database.database import database

from app.common.middleware.request_handle import RequestHandlingMiddleware
from app.common.middleware.sqlalchemy import SQLAlchemyMiddleware


def create_app():
    PROJECT_NAME = "Neubility-Task-Server"
    app = FastAPI(title=PROJECT_NAME)

    database.init_app(app)

    app.add_middleware(RequestHandlingMiddleware)
    app.add_middleware(SQLAlchemyMiddleware)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)
    app.router.route_class = CustomRoute
    app.include_router(base_router)
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
