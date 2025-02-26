import logging

def setup_logger():
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logger()