# Logging Configuration Guide

This document explains the logging system implemented in the FastAPI application.

## Overview

Logging is configured in `app/core/logging_config.py` following the same modular pattern as middleware and exception handlers. The `setup_logging()` function is called from `main.py` to configure all logging components.

## Features

### 1. Multiple Handlers

**Console Handler**: 
- Outputs to stdout with colored formatting in debug mode
- Standard formatting in production
- Always enabled

**File Handler**: 
- Rotating log files (10MB max, 5 backups)
- Detailed formatting with function names and line numbers
- Stored in `logs/` directory

**Error File Handler**: 
- Separate file for ERROR and CRITICAL level logs
- Includes exception tracebacks
- Helps with debugging and monitoring

### 2. Environment-Specific Configuration

**Development Mode** (`DEBUG=True`):
- Colored console output for better readability
- SQL query logging enabled
- More verbose third-party library logging

**Production Mode** (`DEBUG=False`):
- Standard console formatting
- Reduced third-party library noise
- Focus on application-specific logs

### 3. Log Formatting

**Console Format** (Development):
```
2024-01-01 12:00:00,000 - app.core.main - INFO - Starting application
```

**Console Format** (Production):
```
2024-01-01 12:00:00,000 - app.core.main - INFO - Starting application
```

**File Format**:
```
2024-01-01 12:00:00,000 - app.core.main - INFO - lifespan:25 - Starting application
```

### 4. Third-Party Library Configuration

The logging system automatically configures popular libraries:

- **SQLAlchemy**: SQL queries visible in debug mode, warnings only in production
- **Uvicorn**: Access and error logs at INFO level
- **HTTP Libraries**: Reduced to WARNING level to avoid noise
- **AsyncIO**: Warnings only to reduce verbosity

## Usage

### Basic Setup

Logging is automatically configured when the application starts:

```python
from app.core.logging_config import setup_logging, get_logger

# Configure logging (done once at startup)
setup_logging()

# Get logger for your module
logger = get_logger(__name__)

# Use the logger
logger.info("Application started")
logger.error("Something went wrong", exc_info=True)
```

### Getting Loggers

Always use the `get_logger()` function instead of `logging.getLogger()`:

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)
```

### Log Levels

Use appropriate log levels:

```python
logger.debug("Detailed debugging information")
logger.info("General information about application flow")
logger.warning("Something unexpected happened, but app continues")
logger.error("An error occurred that needs attention")
logger.critical("A serious error occurred that may stop the application")
```

### Exception Logging

Always include `exc_info=True` when logging exceptions:

```python
try:
    risky_operation()
except Exception as e:
    logger.error("Operation failed", exc_info=True)
```

## Configuration

### Environment Variables

Control logging behavior through settings:

```python
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
DEBUG = False       # Enables colored output and verbose logging
ENABLE_FILE_LOGGING = True  # Enable/disable file logging
```

### Log Files

Log files are stored in the `logs/` directory:

- `{app_name}.log` - All application logs
- `{app_name}_errors.log` - Error and critical logs only

Files automatically rotate when they reach 10MB, keeping 5 backup files.

## Component-Specific Loggers

Different application components can have specific logging configuration:

```python
LOGGER_CONFIG = {
    'database': {'level': 'INFO'},
    'middleware': {'level': 'INFO'},
    'exception_handlers': {'level': 'WARNING'},
    'api': {'level': 'INFO'},
}
```

## Testing

Test the logging configuration:

```bash
python app/core/test_logging.py
```

This will:
- Test different log levels
- Test component-specific loggers
- Test exception logging
- Create sample log files

## Best Practices

1. **Use Appropriate Levels**: Don't log everything at INFO level
2. **Include Context**: Add relevant information to log messages
3. **Exception Details**: Always use `exc_info=True` for exceptions
4. **Structured Logging**: Consider using structured data in log messages
5. **Performance**: Avoid expensive operations in log messages
6. **Security**: Don't log sensitive information (passwords, tokens, etc.)

## Monitoring and Alerting

In production, consider:

- **Log Aggregation**: Use tools like ELK stack, Fluentd, or cloud logging services
- **Error Alerting**: Set up alerts for ERROR and CRITICAL level logs
- **Log Analysis**: Monitor patterns and trends in application logs
- **Performance Monitoring**: Track slow requests and database queries

## Troubleshooting

### Common Issues

1. **No log files created**: Check file permissions and disk space
2. **Logs not appearing**: Verify LOG_LEVEL setting
3. **Too verbose**: Adjust third-party library log levels
4. **Missing colors**: Ensure DEBUG=True for colored console output

### Debug Logging

Enable debug logging temporarily:

```python
import logging
logging.getLogger('your.module').setLevel(logging.DEBUG)
```

## Adding Custom Loggers

To add logging to new modules:

```python
from app.core.logging_config import get_logger

logger = get_logger(__name__)

def your_function():
    logger.info("Function started")
    try:
        # Your code here
        logger.debug("Processing data")
    except Exception as e:
        logger.error("Function failed", exc_info=True)
        raise
    finally:
        logger.info("Function completed")
```