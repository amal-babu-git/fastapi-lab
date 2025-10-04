# Exception Handlers Guide

This document explains the exception handling system implemented in the FastAPI application.

## Overview

Exception handlers are configured in `app/core/exception_handlers.py` following the same pattern as middleware configuration. The `setup_exception_handlers()` function is called from `main.py` to register all exception handlers.

## Exception Handler Types

### 1. Validation Errors

**RequestValidationError**: Handles FastAPI request validation errors
- Status Code: `422 Unprocessable Entity`
- Returns detailed validation error information

**ValidationError**: Handles Pydantic validation errors
- Status Code: `422 Unprocessable Entity`
- Returns structured validation error details

### 2. Database Errors

**IntegrityError**: Handles database constraint violations
- Status Code: `409 Conflict`
- Common for duplicate key violations, foreign key constraints

**OperationalError**: Handles database connection/operational issues
- Status Code: `503 Service Unavailable`
- Used for connection timeouts, database unavailability

**SQLAlchemyError**: General database error handler
- Status Code: `500 Internal Server Error`
- Catches all other database-related errors

### 3. Application Errors

**ValueError**: Handles invalid input data
- Status Code: `400 Bad Request`
- For business logic validation failures

**PermissionError**: Handles authorization failures
- Status Code: `403 Forbidden`
- For access control violations

**FileNotFoundError**: Handles missing file/resource errors
- Status Code: `404 Not Found`
- For file system or resource access issues

**TimeoutError**: Handles request timeout errors
- Status Code: `408 Request Timeout`
- For operations that exceed time limits

### 4. Global Handler

**Exception**: Catches all unhandled exceptions
- Status Code: `500 Internal Server Error`
- Logs full stack trace for debugging
- Returns generic error message to client

## Error Response Format

All exception handlers return a consistent JSON response format:

```json
{
    "error": "Error Type",
    "detail": "Detailed error message or validation errors",
    "timestamp": "2024-01-01T12:00:00.000000",
    "path": "/api/endpoint"
}
```

## Usage

Exception handlers are automatically configured when the application starts:

```python
from app.core.exception_handlers import setup_exception_handlers

app = FastAPI()
setup_exception_handlers(app)
```

## Logging

All exceptions are logged with appropriate levels:
- `WARNING`: For client errors (validation, permission issues)
- `ERROR`: For server errors (database, system issues)
- Stack traces are included for unhandled exceptions

## Testing

Use the test script to verify exception handlers:

```bash
python app/core/test_exception_handlers.py
```

## Best Practices

1. **Specific Before General**: More specific exception handlers are registered before general ones
2. **Consistent Format**: All handlers return the same JSON structure
3. **Appropriate Logging**: Log at the right level based on error severity
4. **Security**: Don't expose sensitive information in error messages
5. **User-Friendly**: Provide helpful error messages for client-side handling

## Adding New Exception Handlers

To add a new exception handler:

1. Add the handler function in `exception_handlers.py`
2. Register it in the `setup_exception_handlers()` function
3. Follow the consistent response format
4. Add appropriate logging
5. Update this documentation