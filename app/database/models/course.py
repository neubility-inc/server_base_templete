from app.database.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey

from sqlalchemy import func
from sqlalchemy.types import UserDefinedType


class Point(UserDefinedType):
    def get_col_spec(self):
        return "POINT SRID 4326"

    def bind_expression(self, bindvalue):
        return func.ST_GeomFromText(bindvalue, 4326, type_=self)

    def column_expression(self, col):
        return func.ST_AsWKB(col, type_=self)


class Course(Base):
    __tablename__ = "course"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    course_name = Column(String(255), nullable=False)
    hole_name = Column(String(255), nullable=True)
    point = Column(Point, nullable=False)
    service_target_id = Column(
        String(255), ForeignKey("service_target.service_target_id")
    )
