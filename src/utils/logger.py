"""Module with method to create logger."""

import logging

LOG_LEVEL: str = "DEBUG"


def create_logger(logger_name: str) -> logging.Logger:
    """Create logger with optional azure insight connection if defined.

    Args:
        logger_name: Name for the logger e.g. create_logger(__name__).

    Returns:
        Created logger with given name.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s: %(message)s"
    formatter = logging.Formatter(log_format)

    logger = logging.getLogger(logger_name)
    logger.setLevel(LOG_LEVEL)
    if len(logger.handlers):
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
