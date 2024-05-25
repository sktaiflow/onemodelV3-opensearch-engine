import sys
from loguru import logger
from pathlib import Path

# Remove the default loguru handlers
logger.remove()

# Set the log file path
log_file_path = Path(__file__).parent / "logs" / "application.log"

# Create the logs directory if it doesn't exist
log_file_path.parent.mkdir(exist_ok=True)

# Add a file handler for writing logs to the file
file_handler = logger.add(
    str(log_file_path),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {file}:{line} | {message}",
    level="DEBUG",
    rotation="1 week",
    compression="zip",
    enqueue=True,
)

# Add a stream handler for writing logs to the console
console_handler = logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{file}:{line}</cyan> - <level>{message}</level>",
    level="INFO",
    enqueue=True,
)

error_handler = logger.add(
    sys.stderr,
    format="<red>{time:YYYY-MM-DD HH:mm:ss}</red> | <red>{level: <8}</red> | <red>{file}:{line}</red> - <red>{message}</red>",
    level="ERROR",
    enqueue=True,
)

# Optionally, you can add handlers for other logging levels or customize the logging format further

# Export the logger instance for use in other modules
logger = logger.bind(request_id=None)