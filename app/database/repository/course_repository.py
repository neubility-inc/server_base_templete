from .base_repository import BaseRepository
from app.database.models import Course
from app.schema.database import CourseCreate, CourseUpdate


class CourseRepository(BaseRepository[Course, CourseCreate, CourseUpdate]):
    def __init__(self, session):
        super().__init__(session, Course)
