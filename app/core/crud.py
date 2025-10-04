from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base CRUD class with common database operations."""

    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        result = await session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return result.scalars().all()

    async def create(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
        self,
        session: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """Update an existing record."""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        if update_data:
            await session.execute(
                update(self.model)
                .where(self.model.id == db_obj.id)
                .values(**update_data)
            )
            await session.commit()
            await session.refresh(db_obj)
        
        return db_obj

    async def remove(self, session: AsyncSession, *, id: int) -> bool:
        """Delete a record by ID."""
        result = await session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await session.commit()
        return result.rowcount > 0

    async def count(self, session: AsyncSession) -> int:
        """Count total records."""
        from sqlalchemy import func
        result = await session.execute(select(func.count(self.model.id)))
        return result.scalar()