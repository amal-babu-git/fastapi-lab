"""Model template generator."""


def generate_model(module_name: str, class_name: str) -> str:
    """Generate SQLAlchemy model file."""
    return f'''from datetime import datetime, timezone
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class {class_name}(Base):
    """{class_name} model for storing {module_name} information."""

    __tablename__ = "{module_name}s"

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid4, 
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
'''
