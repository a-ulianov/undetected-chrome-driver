"""Undetected Chrome WebDriver package (Selenium based).

This package provides an enhanced Chrome WebDriver with anti-detection capabilities
for web scraping and automation tasks. The main class implements various techniques
to avoid detection by anti-bot systems.

The package includes:
- UndetectedChromeDriver: Main driver class with stealth features
- Network monitoring capabilities
- Cookie and localStorage management
- Headless browser support

Example usage:
>>> from src.undetected_chrome_driver import UndetectedChromeDriver
>>> with UndetectedChromeDriver() as webdriver:
...     webdriver.get('https://example.com')
"""

from .driver import UndetectedChromeDriver
from .logger import Logger
from .config import Config

__author__ = "https://github.com/a-ulianov"
__version__ = "1.0.0"
__license__ = "MIT"

__all__ = [
    'UndetectedChromeDriver', 'Logger', 'Config',
]