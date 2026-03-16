import logging

from core.config import LOGGING_CONFIG


def setup_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=LOGGING_CONFIG["level"],
        format=LOGGING_CONFIG["format"],
    )
    return logging.getLogger(name)
