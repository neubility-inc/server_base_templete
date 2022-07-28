from asyncio import current_task
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, Float

import logging


Base = declarative_base()

class testTable(Base):
    __tablename__ = "testTable"
    test = Column(String(100), nullable=False, primary_key=True)

class SQLAlchemy:
    def __init__(self, app: FastAPI = None, **kwargs) -> None:
        self._engine = None
        self._seesion = None

        if app is not None:
            self.init_app(app=app, **kwargs)

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        RDS_HOSTNAME = 'samsung-control-dev.cfpdcop7a57p.ap-northeast-2.rds.amazonaws.com' #kwargs.get("RDS_HOSTNAME")
        RDS_PORT = 3306 #kwargs.get("RDS_PORT")
        RDS_DB_NAME = 'robot_prod' #kwargs.get("RDS_DB_NAME")
        RDS_USERNAME = 'neubility' #kwargs.get("RDS_USERNAME")
        RDS_PASSWORD = 'neubility' #kwargs.get("RDS_PASSWORD")
        database_url = f"mysql+aiomysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"

        pool_recycle = kwargs.setdefault("DB_POOL_RECYCLE", 900)
        echo = kwargs.setdefault("DB_ECHO", False)

        self._engine = create_async_engine(
            database_url,
            echo=echo,
            pool_recycle=pool_recycle,
            pool_pre_ping=True,
        )
        self._async_session = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)
        self._session = async_scoped_session(self._async_session, scopefunc=current_task)
        
        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB Connected")

        @app.on_event("shutdown")
        def shutdown():
            self._session.close_all()
            self._engine.dispose()
            logging.info("DB Disconnected")

    def create_database(self):
        Base.metadata.create_all(self._engine)

    def drop_table(self):
        Base.metadata.drop_all(self._engine)

    async def get_db(self) -> AsyncSession:
        """
        요청마다 DB 세션 유지 함수
        :return:
        """
        if self._session is None:
            raise Exception("must be called 'init_app'")
        db_session = None
        try:
            db_session = self._session()
            yield db_session
        finally:
            db_session.close()


    @property
    def session(self):
        return self.get_db

    @property
    def engine(self):
        return self._engine


database = SQLAlchemy()