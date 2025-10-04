"""Service template generator."""


def generate_service(module_name: str, class_name: str) -> str:
    """Generate service layer file."""
    return f'''from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logging import get_logger
from .models import {class_name} as {class_name}Model
from .schemas import {class_name}Create, {class_name}Update
from .crud import {module_name}_crud
from .exceptions import {class_name}NotFoundError

# Configure logging
logger = get_logger(__name__)


class {class_name}Service:
    """Service layer for {module_name} business logic."""

    @staticmethod
    async def get_all_{module_name}s(
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[{class_name}Model]:
        """Get all {module_name}s with pagination."""
        return await {module_name}_crud.get_multi(session, skip=skip, limit=limit)

    @staticmethod
    async def get_{module_name}_by_id(
        session: AsyncSession, 
        {module_name}_id: str
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
        """Create a new {module_name}."""
        logger.info(f"Creating {module_name}")
        {module_name} = await {module_name}_crud.create(session, obj_in={module_name}_data)
        logger.info(f"{class_name} created successfully: {{{module_name}.id}}")
        return {module_name}

    @staticmethod
    async def update_{module_name}(
        session: AsyncSession,
        {module_name}_id: str,
        {module_name}_data: {class_name}Update
    ) -> {class_name}Model:
        """Update an existing {module_name}."""
        {module_name} = await {class_name}Service.get_{module_name}_by_id(session, {module_name}_id)
        
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
        {module_name}_id: str
    ) -> None:
        """Delete a {module_name}."""
        {module_name} = await {class_name}Service.get_{module_name}_by_id(session, {module_name}_id)
        
        logger.info(f"Deleting {module_name}: {{{module_name}_id}}")
        await {module_name}_crud.remove(session, id={module_name}_id)
        logger.info(f"{class_name} deleted successfully: {{{module_name}_id}}")
'''
