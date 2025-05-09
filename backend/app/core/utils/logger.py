import os
import sys
from loguru import logger

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_PATH = os.getenv("LOG_PATH", "../../logs/simforge.log")

def setup_logger():
    """Configure the application logger."""
    logger.remove()
    logger.add(sys.stderr, level=LOG_LEVEL)
    logger.add(LOG_PATH, rotation="10 MB", level=LOG_LEVEL)
    return logger

app_logger = setup_logger()