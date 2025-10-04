"""Schema template generator."""


def generate_schemas(module_name: str, class_name: str) -> str:
    """Generate Pydantic schemas file."""
    return f'''from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class {class_name}Base(BaseModel):
    """Base {class_name} schema with common fields."""
    
    name: str = Field(..., min_length=1, max_length=255, description="{class_name} name")
    description: Optional[str] = Field(None, max_length=1000, description="{class_name} description")
    is_active: bool = Field(True, description="Whether the {module_name} is active")


class {class_name}Create({class_name}Base):
    """Schema for creating a new {module_name}."""
    pass


class {class_name}Update(BaseModel):
    """Schema for updating an existing {module_name}."""
    
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    is_active: Optional[bool] = None


class {class_name}({class_name}Base):
    """Schema for {module_name} response with all fields."""
    
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class {class_name}InDB({class_name}):
    """Schema for {module_name} as stored in database."""
    pass
'''
