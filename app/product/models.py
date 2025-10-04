from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Float
from app.core.database import Base


class Product(Base):
    """Product model for storing product information."""

    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)