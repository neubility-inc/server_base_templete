from app.database.database import Base
from sqlalchemy import Column, Integer, String


class Code(Base):
    __tablename__ = "code"

    category = Column(String(255), primary_key=True, nullable=False)
    value = Column(String(255), primary_key=True, nullable=False)
    code = Column(Integer, primary_key=True, nullable=False)
    code_desc = Column(String(255), nullable=True)
    memo = Column(String(255), nullable=True)
