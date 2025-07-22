"""Logger configuration and initialization module.

This module provides a Logger class for configuring and initializing
a customizable logger with both console and file output capabilities.
"""

import logging
import os


class Logger:
    """A customizable logger class with console and file output support.

    This class simplifies logger configuration by providing sensible defaults
    while allowing customization of logging levels, output destinations,
    and log message formatting.

    Args:
        logger_name (str, optional): Name of the logger instance.
            Defaults to 'undetected_chrome_driver'.
        logging_level (int, optional): Logging level (e.g., logging.INFO).
            Defaults to logging.INFO.
        log_to_file (bool, optional): Enable file logging if True.
            Defaults to False.
        logs_dir (str, optional): Directory for log files.
            Defaults to 'logs'.
        log_file (str, optional): Name of the log file.
            Defaults to 'undetected_chrome_driver.log'.
        **kwargs: Additional keyword arguments (currently unused).

    Raises:
        ValueError: If invalid file logging parameters are provided.
    """

    def __init__(
            self,
            logger_name: str = 'undetected_chrome_driver',
            logging_level: int = logging.INFO,
            log_to_file: bool = False,
            logs_dir: str = 'logs',
            log_file: str = 'undetected_chrome_driver.log',
            **kwargs,
    ):
        """Initialize the logger with specified configuration."""
        self.logger: logging.Logger = logging.getLogger(name=logger_name)
        self.logger.setLevel(logging_level)

        # Configure console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging_level)

        # Create formatter with timestamp, logger name, level and message
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)

        # Add console handler to the logger
        self.logger.addHandler(console_handler)

        # Configure file handler if file logging is enabled
        if log_to_file:
            # Validate file logging parameters
            if not isinstance(logs_dir, str) or not isinstance(log_file, str) or not log_file.strip():
                raise ValueError(
                    'Check log file name and path to logs directory are correct.'
                )

            # Ensure logs directory exists
            os.makedirs(logs_dir, exist_ok=True)

            # Create and configure file handler
            file_handler = logging.FileHandler(
                os.path.join(logs_dir, log_file)
            )
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)