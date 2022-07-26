from dataclasses import asdict
from fastapi.applications import FastAPI
from fastapi_utils.tasks import repeat_every

from src.common.config import config
from src.database.database import Base
from src.database.database import database
#from plugin.grandview.skt_grandview import send_robot_device_info_message
#from routes import delivery, index, robot, send_command, service_target, task, robot_status
######################################################

from src.interpreter import RequestHandlingMiddleware


def create_app():
    PROJECT_NAME = "Neubility-Control-Server"
    app = FastAPI(title=PROJECT_NAME)
    
    app.add_middleware(RequestHandlingMiddleware)
    
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