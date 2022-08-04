from pydantic import BaseModel


class CourseBase(BaseModel):
    course_name: str = ""
    hole_name: str = ""
    point: str = None


class CourseCreate(CourseBase):
    service_target_id: str


class CourseUpdate(CourseBase):
    pass
