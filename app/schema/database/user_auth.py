from csv import unregister_dialect
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class UserAuthBase(BaseModel):
    pass


class UserAuthCreate(UserAuthBase):
    user_id: str = ""
    hashed_password: str = ""
    apikey: str = ""
    expire_date: datetime = None
    created_at: datetime = None
    updated_at: datetime = None


class UserAuthUpdate(UserAuthBase):
    pass
