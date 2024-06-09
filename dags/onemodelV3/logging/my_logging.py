from __future__ import annotations
import sys
from loguru import logger as loguru_logger
from pathlib import Path

# Remove the default loguru handlers
loguru_logger.remove()

def configure_logger(date_str: str, log_root_path:str="home/x1112436/shared/x1112436/log/onemodelV3/opensearch"):
    """
    Configure the logger with a dynamic log file path based on the provided date string.
    
    Args:
        date_str (str): The date string to include in the log file path (format: "YY/mm/dd").
    """
    # Parse the date string to create the log file path
    year, month, day = date_str.split('/')
    log_file_path = Path(log_root_path) / "logs" / year / month / day / "application.log"

    # Create the logs directory if it doesn't exist
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Add a file handler for writing logs to the file
    file_handler = loguru_logger.add(
        str(log_file_path),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
        level="ERROR",
        rotation="1 week",
        compression="zip",
        enqueue=True,
    )

    # Add a stream handler for writing logs to the console
    console_handler = loguru_logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>",
        level="INFO",
        enqueue=True,
    )

    debug_handler = loguru_logger.add(
        sys.stderr,
        format="<red>{time:YYYY-MM-DD HH:mm:ss}</red> | <red>{level: <8}</red> | <red>{file}:{line}</red> - <red>{message}</red>",
        level="DEBUG",
        enqueue=True,
    )   
    
    # Optionally, you can add handlers for other logging levels or customize the logging format further

# Export the logger instance for use in other modules
loguru_logger = loguru_logger.bind(request_id=None)