"""Logger configuration and initialization."""

import logging
# import os

LOGGER_NAME = 'Webdriver'
# LOGS_DIR = 'logs'
# LOG_FILE = f'{LOGGER_NAME}.log'
LOGGING_LEVEL = logging.DEBUG

logger: logging.Logger = logging.getLogger(name=LOGGER_NAME)
logger.setLevel(LOGGING_LEVEL)

# Create console handler and set its logging level
console_handler = logging.StreamHandler()
console_handler.setLevel(LOGGING_LEVEL)

# Create formatter and add it to the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

# Add handler to the logger
logger.addHandler(console_handler)

# File logging (commented out)
# file_handler = logging.FileHandler(os.path.join(LOGS_DIR, f'{LOG_FILE}'))
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
#
# logger.addHandler(file_handler)