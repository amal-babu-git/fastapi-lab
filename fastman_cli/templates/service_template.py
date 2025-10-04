"""Service template generator."""


def generate_service(module_name: str, class_name: str) -> str:
    """Generate service layer file."""
    return f'''from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
from .models import {class_name} as {class_name}Model
from .schemas import {class_name}Create, {class_name}Update
from .crud import {module_name}_crud
from .exceptions import (
    {class_name}AlreadyExistsError,
    {class_name}NotFoundError,
)

# Configure logging
logger = get_logger(__name__)


class {class_name}Service:
    """Service layer for {module_name} business logic."""

    @staticmethod
    async def get_all_{module_name}s(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[{class_name}Model]:
        """Get all {module_name}s with pagination."""
        if active_only:
            return await {module_name}_crud.get_active(session, skip=skip, limit=limit)
        return await {module_name}_crud.get_multi(session, skip=skip, limit=limit)

    @staticmethod
    async def get_{module_name}_by_id(
        session: AsyncSession, 
        {module_name}_id: int
    ) -> {class_name}Model:
        """Get a {module_name} by ID."""
        {module_name} = await {module_name}_crud.get(session, {module_name}_id)
        if not {module_name}:
            logger.warning(f"{class_name} not found: {{{module_name}_id}}")
            raise {class_name}NotFoundError({module_name}_id)
        return {module_name}

    @staticmethod
    async def create_{module_name}(
        session: AsyncSession, 
        {module_name}_data: {class_name}Create
    ) -> {class_name}Model:
        """Create a new {module_name} with business logic validation."""
        # Business logic: Check if {module_name} name already exists
        existing_{module_name} = await {module_name}_crud.get_by_name(
            session, 
            {module_name}_data.name
        )
        if existing_{module_name}:
            logger.warning(
                f"{class_name} already exists: {{{module_name}_data.name}}"
            )
            raise {class_name}AlreadyExistsError({module_name}_data.name)

        logger.info(f"Creating {module_name}: {{{module_name}_data.name}}")
        {module_name} = await {module_name}_crud.create(session, obj_in={module_name}_data)
        logger.info(f"{class_name} created successfully: {{{module_name}.id}}")
        return {module_name}

    @staticmethod
    async def update_{module_name}(
        session: AsyncSession,
        {module_name}_id: int,
        {module_name}_data: {class_name}Update
    ) -> {class_name}Model:
        """Update an existing {module_name}."""
        {module_name} = await {class_name}Service.get_{module_name}_by_id(session, {module_name}_id)
        
        # Check if name is being changed and if it conflicts
        if {module_name}_data.name and {module_name}_data.name != {module_name}.name:
            existing = await {module_name}_crud.get_by_name(session, {module_name}_data.name)
            if existing:
                raise {class_name}AlreadyExistsError({module_name}_data.name)
        
        logger.info(f"Updating {module_name}: {{{module_name}_id}}")
        updated_{module_name} = await {module_name}_crud.update(
            session, 
            db_obj={module_name}, 
            obj_in={module_name}_data
        )
        logger.info(f"{class_name} updated successfully: {{{module_name}_id}}")
        return updated_{module_name}

    @staticmethod
    async def delete_{module_name}(
        session: AsyncSession, 
        {module_name}_id: int,
        soft_delete: bool = True
    ) -> None:
        """Delete a {module_name} (soft delete by default)."""
        {module_name} = await {class_name}Service.get_{module_name}_by_id(session, {module_name}_id)
        
        if soft_delete:
            logger.info(f"Soft deleting {module_name}: {{{module_name}_id}}")
            await {module_name}_crud.deactivate(session, {module_name}_id)
        else:
            logger.warning(f"Hard deleting {module_name}: {{{module_name}_id}}")
            await {module_name}_crud.remove(session, id={module_name}_id)
        
        logger.info(f"{class_name} deleted successfully: {{{module_name}_id}}")

    @staticmethod
    async def get_{module_name}_by_name(
        session: AsyncSession, 
        name: str
    ) -> Optional[{class_name}Model]:
        """Get a {module_name} by name."""
        return await {module_name}_crud.get_by_name(session, name)
'''
