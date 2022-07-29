from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, String, Float
from sqlalchemy.sql.expression import null
from app.database.database import Base


class NeubilityApiAccessKeyModel(Base):
    __tablename__ = "neubility_api_access_key"
    user_id = Column(String(255), primary_key=True, nullable=False)
    expiry_date = Column(DateTime(timezone=True), nullable=True, default=0)
    value = Column(String(255), nullable=False)
    token_type = Column(String(255), nullable=False, default="api_key")
