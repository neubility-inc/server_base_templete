from dataclasses import asdict
from fastapi.applications import FastAPI

from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from .common.config import config
from .database.database import database
from .common.error import http_422_error_handler, http_error_handler
from .common.custom_route import CustomRoute
from .routes.urls import router as api_router
from .common.interpreter import RequestHandlingMiddleware
#from .common.interpreter import SQLAlchemyMiddleware


def create_app():
    PROJECT_NAME = "Neubility-Control-Server"
    app = FastAPI(title=PROJECT_NAME)
    
    app.add_middleware(RequestHandlingMiddleware)
    #app.add_middleware(SQLAlchemyMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    #app.add_event_handler("startup", ) # 시작시 실행할 함수 등록
    #app.add_event_handler("shutdown", ) # 종료시 실행할 함수 등록

    app.add_exception_handler(HTTPException, http_error_handler)
    app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)
    app.router.route_class = CustomRoute
    app.include_router(
        api_router,
        prefix="/api"
    )

    config_dict = asdict(config)
    database.init_app(app, **config_dict)
    

    """
    app.include_router(index.router)
    app.include_router(robot.router)
    app.include_router(delivery.router)
    app.include_router(task.router)
    app.include_router(service_target.router)
    app.include_router(robot_status.router)
    app.include_router(send_command.router)
    """

    return app


app = create_app()


# @app.on_event("startup")
# @repeat_every(seconds=60)
# def waiting_time_exceed_task() -> None:
#     send_robot_device_info_message(next(database.session()))