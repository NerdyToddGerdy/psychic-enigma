"""
Logging configuration for RPG Hex Grid Game
Sets up centralized logging with file and console handlers
"""

import logging
import logging.handlers
from pathlib import Path
from config import config


def setup_logging():
    """
    Configure application-wide logging

    Creates both file and console handlers with appropriate formatters
    File handler includes rotation to prevent log files from growing too large
    """
    # Get root logger
    root_logger = logging.getLogger()

    # Clear any existing handlers
    root_logger.handlers.clear()

    # Set log level from config
    log_level = getattr(logging, config.LOG_LEVEL.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    # Create formatters
    detailed_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_formatter = logging.Formatter(
        fmt='%(levelname)s: %(message)s'
    )

    # File handler with rotation
    log_file_path = config.get_abs_path(config.LOG_FILE)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_file_path,
        maxBytes=config.LOG_MAX_BYTES,
        backupCount=config.LOG_BACKUP_COUNT,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)  # File logs everything
    file_handler.setFormatter(detailed_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(console_formatter)

    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # Log initialization
    root_logger.info("=" * 70)
    root_logger.info(f"{config.APP_NAME} - Logging initialized")
    root_logger.info(f"Log Level: {config.LOG_LEVEL}")
    root_logger.info(f"Log File: {log_file_path}")
    root_logger.info("=" * 70)

    return root_logger


def get_logger(name):
    """
    Get a logger instance for a specific module

    Args:
        name (str): Usually __name__ of the calling module

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(name)


# Initialize logging when this module is imported
setup_logging()