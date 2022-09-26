from csv import unregister_dialect
from ssl import create_default_context
from app.database.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey


class UserAuth(Base):
    __tablename__ = "user_auth"

    user_id = Column(String(255), primary_key=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    apikey = Column(String(255), nullable=True)
    expire_date = Column(DateTime(timezone=True), nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), nullable=False, default=0)
    updated_at = Column(DateTime(timezone=True), nullable=False, default=0)
