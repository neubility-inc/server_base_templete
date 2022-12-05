from app.routes.user_auth.user_auth_handler import UserAuthHandler
from fastapi_utils.cbv import cbv as class_based_view
from fastapi_utils.inferring_router import InferringRouter
from app.routes.user_auth import UserAuthBaseController
from fastapi import HTTPException, Depends, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
import secrets
from app.utils.auth import auth_manager
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.database.models import user_auth

user_auth_router = InferringRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


@class_based_view(user_auth_router)
class AuthController(UserAuthBaseController):
    def __init__(self, auth_handler: UserAuthHandler = Depends(UserAuthHandler)):
        self._auth_handler = auth_handler
