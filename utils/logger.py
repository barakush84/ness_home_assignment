import logging
from pathlib import Path
from datetime import datetime


# Create logs directory if it doesn't exist
logs_dir = Path(__file__).parent.parent / 'logs'
logs_dir.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger('test_logger')
logger.setLevel(logging.DEBUG)

# Create formatters
formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(filename)-25s:%(lineno)-3d - %(message)s')

# File handler
log_file = logs_dir / f'test_log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
file_handler = logging.FileHandler(str(log_file))
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)


def get_logger():
    """Get the configured logger instance for the test framework.

    Returns:
        logging.Logger: The logger instance.
    """
    return logger
