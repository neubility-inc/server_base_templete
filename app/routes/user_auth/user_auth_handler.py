from app.database.database import transactional
from app.routes.user_auth import UserAuthBaseHandler
from app.schema.database.user_auth import UserAuthCreate
from app.database.repository.user_auth_repository import UserAuthRepository
from app.database.database import database
from app.utils.auth import auth_manager


class UserAuthHandler(UserAuthBaseHandler):
    def __init__(self):
        self._user_auth_repository = UserAuthRepository(database.session)

    async def get_user_auth_by_user_id(self, user_id):
        return await self._user_auth_repository.get_user_auth_by_user_id(user_id)

    async def get_user_auth_by_apikey(self, api_key):
        return await self._user_auth_repository.get_user_auth_by_apikey(api_key)

    async def check_user_auth(self, key_value):
        user_auth = await self.get_user_auth_by_apikey(key_value)
        if user_auth is not None and user_auth.apikey == key_value:
            return True
        return False

    @transactional
    async def insert_user_auth(self, user_data: dict):
        res = await self._user_auth_repository.insert_user_auth(
            UserAuthCreate(
                user_id=user_data.get("user_id"),
                hashed_password=auth_manager.get_hashed_password(
                    user_data.get("password")
                ),
            )
        )
        return UserAuthPostResponse(user_id=res.user_id, apikey=res.apikey)
