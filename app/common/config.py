import os

from pydantic import BaseSettings
from dotenv import load_dotenv


FILE_DIR = os.path.dirname(__file__)
load_dotenv()


class BaseConfig(BaseSettings):
    APP_ENV: str = os.getenv("APP_ENV", "local")

    class Config:
        env_file = ".env"


class ServerConfig(BaseConfig):
    API_ENV: str = os.getenv("API_ENV", "local")
<<<<<<< HEAD
    SERVER_NAME: str = os.getenv("SERVER_NAME", "Neubility Robot Server")
    SERVER_APP_FILE: str = os.getenv("SERVER_APP_FILE", "robot_api")
=======
    SERVER_NAME: str = os.getenv("SERVER_NAME", "Neubility Task Server")
    SERVER_APP_FILE: str = os.getenv("SERVER_APP_FILE", "task_api")
>>>>>>> 9249abc9db8bc7f8ef1822ff5a67dfbf24dae4f9
    SERVER_HOST: str = os.getenv("SERVER_HOST", "127.0.0.1")
    SERVER_PORT: int = os.getenv("SERVER_PORT", 8000)
    SERVER_VERSION: str = os.getenv("SERVER_VERSION", "1.0.0")

<<<<<<< HEAD
    RDS_DB_NAME: str = os.getenv("RDS_DB_NAME", "robot_prod")
=======
    RDS_DB_NAME: str = os.getenv("RDS_DB_NAME", "task")
>>>>>>> 9249abc9db8bc7f8ef1822ff5a67dfbf24dae4f9
    RDS_HOSTNAME: str = os.getenv(
        "RDS_HOSTNAME",
        "order-database-dev.cfpdcop7a57p.ap-northeast-2.rds.amazonaws.com",
    )
    RDS_PORT: int = os.getenv("RDS_PORT", 3306)
    RDS_USERNAME: str = os.getenv("RDS_USERNAME", "admin")
    RDS_PASSWORD: str = os.getenv("RDS_PASSWORD", "Sbqlfflxl10!")
    RDS_POOL_RECYCLE: int = os.getenv("RDS_POOL_RECYCLE", 900)
    RDS_ECHO: bool = os.getenv("RDS_ECHO", False)

    TEST: bool = bool(os.getenv("TEST", False))

    GLOBAL_PLANNING_SERVER_URL: str = "https://api.neubie.ai/planning"

<<<<<<< HEAD
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_PORT: int = os.getenv("REDIS_PORT", 6379)

    DISPATCH_SERVER_URL: str = os.getenv(
        "DISPATCH_SERVER_URL", "http://dev.control.neubie.ai:9000"
    )

=======
>>>>>>> 9249abc9db8bc7f8ef1822ff5a67dfbf24dae4f9
    class Config:
        env_file = ".env"


"""
 로컬 테스트 시 env 폴더에 {APP_ENV}.env 파일 생성 후 테스트 진행
"""
config = ServerConfig(_env_file=f"{FILE_DIR}/env/{BaseConfig().APP_ENV}.env")
