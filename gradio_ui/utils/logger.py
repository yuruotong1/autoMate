"""Logging configuration for autoMate"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime

# Create logs directory
LOGS_DIR = Path.home() / ".automate" / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def setup_logging(
    name: str = "automate",
    level: str = "INFO",
    log_file: bool = True,
    log_console: bool = True,
) -> logging.Logger:
    """
    Setup logging configuration.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Whether to log to file
        log_console: Whether to log to console

    Returns:
        Configured logger
    """
    logger = logging.getLogger(name)

    # Set level from environment or parameter
    env_level = os.getenv("LOG_LEVEL", level).upper()
    logger.setLevel(getattr(logging, env_level, logging.INFO))

    # Remove existing handlers
    logger.handlers = []

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    if log_console:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, env_level, logging.INFO))
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # File handler
    if log_file:
        log_file_path = LOGS_DIR / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"

        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(getattr(logging, env_level, logging.INFO))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Create default logger
logger = setup_logging()


class ContextFilter(logging.Filter):
    """Filter to add context to log records"""

    def __init__(self, context_dict: dict = None):
        super().__init__()
        self.context_dict = context_dict or {}

    def filter(self, record):
        for key, value in self.context_dict.items():
            setattr(record, key, value)
        return True


def add_context(logger: logging.Logger, context: dict) -> None:
    """
    Add context information to logger.

    Args:
        logger: Logger instance
        context: Context dictionary
    """
    context_filter = ContextFilter(context)
    for handler in logger.handlers:
        handler.addFilter(context_filter)


def create_task_logger(task_id: str) -> logging.Logger:
    """
    Create logger for specific task.

    Args:
        task_id: Task identifier

    Returns:
        Task-specific logger
    """
    task_logger = logging.getLogger(f"automate.task.{task_id}")

    # Create task-specific file handler
    log_file = LOGS_DIR / f"task_{task_id}_{datetime.now().isoformat()}.log"

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    task_logger.addHandler(handler)

    return task_logger


# Module-level loggers for different components
vision_logger = logging.getLogger("automate.vision")
agent_logger = logging.getLogger("automate.agent")
tool_logger = logging.getLogger("automate.tool")
executor_logger = logging.getLogger("automate.executor")
api_logger = logging.getLogger("automate.api")
