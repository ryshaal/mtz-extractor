"""
Logging utilities
Provides logging configuration and setup
"""

import logging
import platform
import psutil
from pathlib import Path
from datetime import datetime


def setup_logger(name: str) -> logging.Logger:
    """
    Set up and configure logger with system information
    
    Args:
        name: Logger name (usually module name)
    
    Returns:
        Configured logger instance
    """
    # Create logs folder if it doesn't exist
    log_folder = Path("logs")
    log_folder.mkdir(exist_ok=True)

    # Generate timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_folder / f"{name}_{timestamp}.log"

    # Create logger
    logger = logging.getLogger(f"{name}_{timestamp}")
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    # Create file handler
    file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(file_handler)

    # Ensure log doesn't duplicate to root logger
    logger.propagate = False

    # Log system information
    _log_system_info(logger, log_file)

    return logger


def _log_system_info(logger: logging.Logger, log_file: Path) -> None:
    """
    Log system information to the log file
    
    Args:
        logger: Logger instance
        log_file: Path to log file
    """
    try:
        # Get memory information
        memory_info = psutil.virtual_memory()

        # Log system information
        logger.info("=" * 60)
        logger.info("MTZ Tool - System Information")
        logger.info("=" * 60)
        logger.info(f"System: {platform.system()} {platform.release()}")
        logger.info(f"CPU Architecture: {platform.machine()}")
        logger.info(f"Python Version: {platform.python_version()}")
        logger.info(f"Memory: Total={memory_info.total / (1024 ** 3):.2f} GB, "
                   f"Used={memory_info.used / (1024 ** 3):.2f} GB, "
                   f"Available={memory_info.available / (1024 ** 3):.2f} GB, "
                   f"Usage={memory_info.percent}%")
        logger.info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"Log file: {log_file}")
        logger.info("=" * 60)
    except Exception as e:
        logger.warning(f"Failed to log system information: {str(e)}")