from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Base CRUD class with common database operations.

    This class provides a reusable, type-safe interface for CRUD operations
    on SQLAlchemy models using Generic types for full type inference.

    Based on best practices from FastAPI's full-stack template.
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUD object with a SQLAlchemy model class.

        Args:
            model: A SQLAlchemy model class (table definition)
        """
        self.model = model

    async def get(self, session: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a single record by ID.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            Model instance or None if not found
        """
        result = await session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self, session: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            session: Database session
            skip: Number of records to skip (offset)
            limit: Maximum number of records to return

        Returns:
            List of model instances ordered by ID
        """
        result = await session.execute(
            select(self.model).offset(skip).limit(
                limit).order_by(self.model.id)
        )
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            session: Database session
            obj_in: Pydantic schema with creation data

        Returns:
            Created model instance with generated ID
        """
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
        """
        Update an existing record.

        Args:
            session: Database session
            db_obj: Existing model instance to update
            obj_in: Pydantic schema or dict with update data

        Returns:
            Updated model instance

        Note:
            Uses exclude_unset=True to only update provided fields (partial updates)
        """
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
        """
        Delete a record by ID.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            True if record was deleted, False if not found
        """
        result = await session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await session.commit()
        return result.rowcount > 0

    async def count(self, session: AsyncSession) -> int:
        """
        Count total number of records.

        Args:
            session: Database session

        Returns:
            Total count of records in the table
        """
        result = await session.execute(select(func.count(self.model.id)))
        return result.scalar() or 0

    async def exists(self, session: AsyncSession, id: Any) -> bool:
        """
        Check if a record exists by ID.

        Args:
            session: Database session
            id: Primary key value

        Returns:
            True if record exists, False otherwise
        """
        result = await session.execute(
            select(self.model.id).where(self.model.id == id)
        )
        return result.scalar_one_or_none() is not None
