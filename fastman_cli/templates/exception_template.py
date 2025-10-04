"""Exception template generator."""


def generate_exceptions(module_name: str, class_name: str) -> str:
    """Generate custom exceptions file."""
    return f'''"""
Custom exceptions for the {module_name} module.

These exceptions provide specific error types for business logic violations,
making error handling more explicit and maintainable.
"""


class {class_name}Exception(Exception):
    """Base exception for all {module_name}-related errors."""
    pass


class {class_name}NotFoundError({class_name}Exception):
    """Raised when a {module_name} is not found."""

    def __init__(self, identifier):
        self.identifier = identifier
        super().__init__(f"{class_name} with identifier '{{identifier}}' not found")


class {class_name}AlreadyExistsError({class_name}Exception):
    """Raised when attempting to create a {module_name} that already exists."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"{class_name} with name '{{name}}' already exists")


class Invalid{class_name}DataError({class_name}Exception):
    """Raised when {module_name} data is invalid."""

    def __init__(self, message: str):
        super().__init__(f"Invalid {module_name} data: {{message}}")
'''
