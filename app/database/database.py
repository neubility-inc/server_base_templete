from asyncio import current_task
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_scoped_session,
)
from sqlalchemy.exc import IntegrityError

from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import logging
from app.common.config import config
from contextvars import ContextVar, Token

from app.common.exception.db_exception import ConflictException

Base = declarative_base()


class DatabaseSession:
    def __init__(self, app: FastAPI = None, **kwargs) -> None:
        RDS_HOSTNAME = config.RDS_HOSTNAME
        RDS_PORT = config.RDS_PORT
        RDS_DB_NAME = config.RDS_DB_NAME
        RDS_USERNAME = config.RDS_USERNAME
        RDS_PASSWORD = config.RDS_PASSWORD

        self._database_url = f"mysql+aiomysql://{RDS_USERNAME}:{RDS_PASSWORD}@{RDS_HOSTNAME}:{RDS_PORT}/{RDS_DB_NAME}"
        self._pool_recycle = config.RDS_POOL_RECYCLE
        self._echo = config.RDS_ECHO

        self._engine = None
        self._session = None
        self._session_context: ContextVar[str] = ContextVar("session_context")
        if app is not None:
            self.init_app(app=app, **kwargs)

    def get_session_id(self) -> str:
        return self._session_context.get()

    def set_session_context(self, session_id: str) -> Token:
        return self._session_context.set(session_id)

    def reset_session_context(self, context: Token):
        self._session_context.reset(context)

    def create_engine(self):
        self._engine = create_async_engine(
            self._database_url,
            echo=self._echo,
            pool_recycle=self._pool_recycle,
            pool_pre_ping=self._echo,
        )

    def create_session(self):
        async_session_factory = sessionmaker(bind=self._engine, class_=AsyncSession)
        self._session = async_scoped_session(
            session_factory=async_session_factory, scopefunc=self.get_session_id
        )

    def init_app(self, app: FastAPI, **kwargs):
        """
        DB 초기화 함수
        :param app: FastAPI 인스턴스
        :param kwargs:
        :return:
        """
        self.create_engine()
        self.create_session()

        @app.on_event("startup")
        def startup():
            self._engine.connect()
            logging.info("DB Connected")

        @app.on_event("shutdown")
        async def shutdown():
            # await self._session.close_all()
            await self._engine.dispose()
            logging.info("DB Disconnected")

    async def create_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        # await database.session.commit()

    async def drop_tables(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

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
        return self._session

    @property
    def engine(self):
        return self._engine


database = DatabaseSession()

from functools import wraps


def transactional(function):
    @wraps(function)
    async def decorator(*args, **kwargs):
        try:
            result = await function(*args, **kwargs)
            await database.session.commit()

        except IntegrityError:
            raise ConflictException
        except Exception as e:
            await database.session.rollback()
            raise e
        return result

    return decorator
