from typing import Generic, TypeVar, Union, Dict, Any, Type

from app.database.database import Base
from pydantic import BaseModel
from sqlalchemy import select

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, session, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def create(self, create_schema: CreateSchemaType) -> ModelType:
        db_obj = self.model(**create_schema.dict())

        self.session.add(db_obj)

        return db_obj

    async def delete(self, db_obj) -> ModelType:
        await self.session.delete(db_obj)

        return db_obj

    async def save(
        self, db_obj: ModelType, update_schema: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        if not isinstance(update_schema, dict):
            update_schema = update_schema.dict(exclude_unset=True)
        obj_data = db_obj.__dict__

        for field in obj_data:
            if field in update_schema:
                setattr(db_obj, field, update_schema[field])

        # self.session.merge(db_obj)

        return db_obj
