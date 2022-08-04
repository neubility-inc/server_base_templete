from os import getenv
#from dotenv import load_dotenv


def config_loader(config):
    #load_dotenv(verbose=True)

    config.API_ENV: str = getenv("API_ENV")
    config.RDS_HOSTNAME: str = getenv("RDS_HOSTNAME")
    config.RDS_PORT: str = getenv("RDS_PORT")
    config.RDS_DB_NAME: str = getenv("RDS_DB_NAME")
    config.RDS_USERNAME: str = getenv("RDS_USERNAME")
    config.RDS_PASSWORD: str = getenv("RDS_PASSWORD")
    config.ORDER_SERVER_URL: str = getenv("ORDER_SERVER_URL")
    config.GLOBAL_PLANNING_SERVER_URL: str = getenv("GLOBAL_PLANNING_SERVER_URL")
