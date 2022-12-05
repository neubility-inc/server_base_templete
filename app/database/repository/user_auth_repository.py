from sqlalchemy.exc import NoResultFound
from sqlalchemy import select, insert, update, delete
from app.schema.database.user_auth import UserAuthCreate
from .base_repository import BaseRepository

from app.database.models.user_auth import UserAuth
from app.schema.database.user_auth import UserAuthCreate, UserAuthUpdate

from uuid import uuid4
from datetime import datetime, timedelta
from app.utils.auth import auth_manager


class UserAuthRepository(BaseRepository[UserAuth, UserAuthCreate, UserAuthUpdate]):
    def __init__(self, session):
        super().__init__(session, UserAuth)

    async def get_user_auth_by_user_id(self, user_id: str):
        try:
            return (
                (
                    await self.session.execute(
                        select(UserAuth).where(UserAuth.user_id == user_id)
                    )
                )
                .scalars()
                .one()
            )
        except NoResultFound as e:
            return None

    async def get_user_auth_by_apikey(self, apikey: str):
        try:
            return (
                (
                    await self.session.execute(
                        select(UserAuth).where(UserAuth.apikey == apikey)
                    )
                )
                .scalars()
                .one()
            )
        except NoResultFound as e:
            return None

    async def insert_user_auth(self, user_auth_create: UserAuthCreate):
        user_id = user_auth_create.user_id
        user_auth_create.apikey = auth_manager.create_access_token(user_id, 60 * 24 * 7)
        user_auth_create.expire_date = datetime.now() + timedelta(days=365)
        user_auth_create.created_at = datetime.now()
        user_auth_create.updated_at = datetime.now()

        try:
            self.create(user_auth_create)
        except Exception as e:
            return False
        return user_auth_create
