"""Schema template generator."""


def generate_schemas(module_name: str, class_name: str) -> str:
    """Generate Pydantic schemas file."""
    return f'''from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class {class_name}Base(BaseModel):
    """Base {class_name} schema with common fields."""
    pass


class {class_name}Create({class_name}Base):
    """Schema for creating a new {module_name}."""
    pass


class {class_name}Update(BaseModel):
    """Schema for updating an existing {module_name}."""
    pass


class {class_name}({class_name}Base):
    """Schema for {module_name} response with all fields."""
    
    id: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class {class_name}InDB({class_name}):
    """Schema for {module_name} as stored in database."""
    pass
'''
