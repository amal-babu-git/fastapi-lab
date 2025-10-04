"""
Custom exceptions for the category module.

These exceptions provide specific error types for business logic violations,
making error handling more explicit and maintainable.
"""


class CategoryException(Exception):
    """Base exception for all category-related errors."""
    pass


class CategoryNotFoundError(CategoryException):
    """Raised when a category is not found."""

    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(f"Category with identifier '{identifier}' not found")


class CategoryAlreadyExistsError(CategoryException):
    """Raised when attempting to create a category that already exists."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Category with name '{name}' already exists")


class InvalidCategoryDataError(CategoryException):
    """Raised when category data is invalid."""

    def __init__(self, message: str):
        super().__init__(f"Invalid category data: {message}")
