from .base_repository import BaseRepository
from app.database.models import Code
from app.schema.database import CodeCreate, CodeUpdate


class CodeRepository(BaseRepository[Code, CodeCreate, CodeUpdate]):
    def __init__(self, session):
        super().__init__(session, Code)
