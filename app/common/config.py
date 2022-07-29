import platform

from dataclasses import dataclass
from os import path

base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))


@dataclass
class BaseConfigModel:
    """
    Basic Configuration
    """

    BASE_DIR: str = base_dir
    DB_POOL_RECYCLE: int = 900
    DB_ECHO: bool = False
    DEBUG: bool = False


@dataclass
class ConfigModel(BaseConfigModel):
    TRUSTED_HOSTS = ["*"]
    ALLOWED_SITE = ["*"]
    API_ENV: str = ""
    RDS_HOSTNAME: str = ""
    RDS_PORT: str = ""
    RDS_DB_NAME: str = ""
    RDS_USERNAME: str = ""
    RDS_PASSWORD: str = ""
    ROBOT_CONTROL_ADDRESS: str = ""
    ROBOT_CONTROL_PORT: str = ""
    ORDER_SERVER_URL: str = ""
    GLOBAL_PLANNING_SERVER_URL: str = ""


config = ConfigModel()
if platform.system() == "Linux":
    from app.common.linux_config import config_loader

elif platform.system() == "Windows":
    from app.common.windows_config import config_loader

elif platform.system() == "Darwin":
    from app.common.darwin_config import config_loader

config_loader(config)
