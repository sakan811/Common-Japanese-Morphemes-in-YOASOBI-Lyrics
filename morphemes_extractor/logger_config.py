import logging
import sys


def setup_logger(name=None, level=logging.WARNING):
    """
    Set up and configure logger
    
    Args:
        name: Name of the logger (None for root logger)
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers if any
    if logger.handlers:
        logger.handlers.clear()
    
    # Create handlers
    handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(handler)
    
    return logger
