"""
Test script to verify logging configuration is working correctly.
"""
from app.core.logging import setup_logging, get_logger
import logging


def test_logging_configuration():
    """Test that logging is properly configured."""

    # Setup logging
    setup_logging()

    # Get different loggers
    app_logger = get_logger(__name__)
    db_logger = get_logger("app.core.database")
    api_logger = get_logger("app.apis.v1")

    # Test different log levels
    app_logger.debug("This is a debug message")
    app_logger.info("✓ Info level logging working")
    app_logger.warning("⚠ Warning level logging working")
    app_logger.error("✗ Error level logging working")

    # Test different component loggers
    db_logger.info("✓ Database logger working")
    api_logger.info("✓ API logger working")

    # Test exception logging
    try:
        raise ValueError("Test exception for logging")
    except ValueError as e:
        app_logger.error("Exception caught and logged", exc_info=True)

    print("✓ All logging tests completed!")
    print("Check the logs/ directory for log files")


if __name__ == "__main__":
    test_logging_configuration()
