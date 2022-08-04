from app.database.database import Base
from sqlalchemy import Column, String


class ServiceTarget(Base):
    __tablename__ = "service_target"

    service_target_id = Column(String(255), primary_key=True, nullable=False)
    description = Column(String(255), nullable=True)
    service_target_name = Column(String(255), nullable=True)
