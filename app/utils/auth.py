from passlib.context import CryptContext
import os
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt

# 나중에 os로 뺴야함 #os.environ["JWT_SECRET_KEY"]
# os.environ["JWT_REFRESH_SECRET_KEY"]


class AuthManager:
    def __init__(self):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # 1 year
        self.ALGORITHM = "HS256"
        self.JWT_SECRET_KEY = (
            "da567dd4e9673941ab75a4cc16ac6f61824d5d300b8a41ac5e762cf7cb145030"
        )
        self.JWT_REFRESH_SECRET_KEY = "00373e86dc28bc2ce25544bde6782033ea8723c3104ef3ea428c55fb9031a57e59d5c49fed154b9f59f7a36a29e821885d843948a108e4eae1842281b44d4d88"  # os.environ["JWT_REFRESH_SECRET_KEY"]  # should be kept secret
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def decode_jwt(self, token: str):
        return jwt.decode(
            token, self.JWT_REFRESH_SECRET_KEY, algorithms=[self.ALGORITHM]
        )


auth_manager = AuthManager()
