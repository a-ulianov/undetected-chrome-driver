"""
Configuration module for the Undetected Chrome WebDriver.

This module provides a centralized configuration class with default settings
for the Chrome WebDriver instance, including browser options, user agent,
performance logging, and logger configuration.

The Config class serves as a single source of truth for all configurable
parameters, making it easier to maintain and modify driver settings.
"""

import logging


class Config:
    """
    Centralized configuration for Undetected Chrome WebDriver.

    This class contains default settings for:
    - Browser user agent
    - Chrome driver options
    - Performance logging
    - Logger configuration

    Attributes:
        user_agent (str): Default user agent string for the browser.
        chrome_driver_options (list[str]): List of Chrome command line options.
        enable_performance_logging (bool): Flag to enable network request logging.
        logger_name (str): Name identifier for the logger instance.
        logging_level (int): Default logging level (e.g., logging.INFO).
        log_to_file (bool): Enable file logging when True.
        logs_dir (str): Directory path for log file storage.
        log_file (str): Name of the log file.
    """

    # Browser configuration
    user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    """Default user agent string mimicking a recent Chrome browser on Windows."""

    chrome_driver_options: list[str] = [
        '--headless=new',
        '--disable-blink-features=AutomationControlled',
        '--start-maximized',
        '--disable-dev-shm-usage',
        '--disable-extensions',
        '--no-sandbox',
        '--ignore-certificate-errors',
        '--enable-javascript',
        '--log-level=3',
        '--disable-logging',
    ]
    """List of Chrome command line options for optimal undetected operation."""

    enable_performance_logging: bool = False
    """When True, enables network request monitoring through performance logs."""

    # Logger configuration
    logger_name: str = 'undetected_chrome_driver'
    """Default name for the logger instance."""

    logging_level: int = logging.INFO
    """Default logging level (INFO). Can be set to DEBUG for more verbose output."""

    log_to_file: bool = False
    """When True, enables logging to file in addition to console output."""

    logs_dir: str = 'logs'
    """Directory where log files will be stored if file logging is enabled."""

    log_file: str = 'undetected_chrome_driver.log'
    """Default name for the log file if file logging is enabled."""