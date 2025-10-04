"""
Custom exceptions for the product module.

These exceptions provide specific error types for business logic violations,
making error handling more explicit and maintainable.
"""


class ProductException(Exception):
    """Base exception for all product-related errors."""
    pass


class ProductNotFoundError(ProductException):
    """Raised when a product is not found."""

    def __init__(self, product_id: int):
        self.product_id = product_id
        super().__init__(f"Product with ID {product_id} not found")


class ProductAlreadyExistsError(ProductException):
    """Raised when attempting to create a product that already exists."""

    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Product with name '{name}' already exists")


class InvalidPriceError(ProductException):
    """Raised when a product price is invalid."""

    def __init__(self, price: float, message: str = None):
        self.price = price
        default_message = f"Invalid price: {price}. Price must be at least $0.01"
        super().__init__(message or default_message)


class InvalidPriceRangeError(ProductException):
    """Raised when price range parameters are invalid."""

    def __init__(self, min_price: float, max_price: float):
        self.min_price = min_price
        self.max_price = max_price
        super().__init__(
            f"Invalid price range: min={min_price}, max={max_price}. "
            "Prices must be non-negative and min cannot be greater than max"
        )


class InsufficientStockError(ProductException):
    """Raised when attempting to reduce stock below zero."""

    def __init__(self, product_id: int, current_quantity: int, requested_change: int):
        self.product_id = product_id
        self.current_quantity = current_quantity
        self.requested_change = requested_change
        super().__init__(
            f"Insufficient stock for product {product_id}. "
            f"Current: {current_quantity}, Requested change: {requested_change}"
        )


class InvalidStockThresholdError(ProductException):
    """Raised when stock threshold is invalid."""

    def __init__(self, threshold: int):
        self.threshold = threshold
        super().__init__(
            f"Invalid stock threshold: {threshold}. Must be non-negative")
