import logging
import os

from core.settings import settings


def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger with console + file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))

    # Avoid adding duplicate handlers
    if logger.handlers:
        return logger

    os.makedirs(settings.LOG_DIR, exist_ok=True)

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    console.setFormatter(console_fmt)
    logger.addHandler(console)

    # File handler
    file_handler = logging.FileHandler(os.path.join(settings.LOG_DIR, "test_automation.log"))
    file_handler.setLevel(logging.DEBUG)
    file_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    return logger
