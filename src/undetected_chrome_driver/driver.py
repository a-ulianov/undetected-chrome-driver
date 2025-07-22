import json
from typing import Any, Optional, Union

import undetected_chromedriver as uc
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
import selenium_stealth
from webdriver_manager.chrome import ChromeDriverManager

from .logger import Logger


class UndetectedChromeDriver:
    """
    Manages an undetected Chrome WebDriver (Selenium based) with enhanced stealth features.

    This class configures and initializes a headless Chrome browser that avoids detection
    by common anti-bot measures. It extends Selenium webdiver methods with methods to retrieve
    network requests, cookies and local storage.

    Attributes:
        _user_agent: Default user agent string
        _options: List of default Chrome options
        _service_args: List of default service arguments for ChromeDriver

    Examples:
    >>> with UndetectedChromeDriver() as driver:
    ...     driver.get('https://example.com')
    """

    _user_agent: str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    _options: list[str] = [
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
    _service_args: list[str] = ['--disable-logging', '--silent']

    def __init__(
            self,
            user_agent: Optional[str] = None,
            chrome_driver_options: Optional[list[str]] = None,
            enable_performance_logging: bool = False,
            **kwargs,
    ) -> None:
        """
        Initializes the undetected Chrome driver with stealth configuration.

        Args:
            user_agent: Custom user agent string. Uses default if None
            chrome_driver_options: Custom Chrome options. Uses defaults if None
            enable_performance_logging: Enable performance logging for network monitoring
        """
        self.user_agent: str = user_agent if user_agent else self._user_agent
        self._is_performance_logging_enabled: bool = enable_performance_logging

        # Configure capabilities for performance logging if enabled
        self.capabilities: dict[str, Any] = DesiredCapabilities.CHROME
        if self._is_performance_logging_enabled:
            self.capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}

        # Set up Chrome options
        self.options: uc.ChromeOptions = uc.ChromeOptions()
        self.options.add_argument(f'user-agent={self.user_agent}')

        # Apply default options if no custom options provided
        options_list: list[str] = chrome_driver_options if chrome_driver_options else self._options
        for option in options_list:
            self.options.add_argument(option)

        # Initialize Chrome service and driver
        self.service: Service = Service(
            ChromeDriverManager().install(),
            service_args=self._service_args,
        )
        self.driver: uc.Chrome = uc.Chrome(
            service=self.service,
            options=self.options,
            desired_capabilities=self.capabilities
        )

        # Override navigator.webdriver and simulate regular browser environment
        self.driver.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {
                'source': """
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    window.chrome = {
                        runtime: {},
                    };
                """
            }
        )

        # Apply stealth configurations to avoid bot detection
        selenium_stealth.stealth(
            self.driver,
            languages=['en-US', 'en'],          #type: ignore
            user_agent=self.user_agent,
            vendor='Google Inc.',
            platform='Win64',
            webgl_vendor='Intel Inc.',
            renderer='Intel Iris OpenGL Engine',
            fix_hairline=True
        )

        self.logger = Logger(**kwargs).logger

    @classmethod
    def from_obj(cls, obj: Any) -> 'UndetectedChromeDriver':

        attrs: dict[str, Any] = {}

        for attr_name in dir(obj):
            # Exclude methods and private attributes
            if attr_name.startswith('__') or callable(getattr(obj, attr_name)):
                continue

            attrs[attr_name] = getattr(obj, attr_name)

        return cls(**attrs)

    def get_sent_requests(self) -> list[dict]:
        """
        Retrieves network request logs from performance logs.

        Returns:
            List of dictionaries containing network request data
        """
        if not self._is_performance_logging_enabled:
            self.logger.warning('Performance logging is disabled')
            return []

        try:
            # Retrieve performance logs
            logs: list[dict] = self.driver.get_log('performance')
        except Exception as e:
            self.logger.error(f'Error retrieving performance logs: {str(e)}')
            return []

        # Filter for network request events
        return [
            log for log in logs
            if json.loads(log['message']).get('message', {}).get('method') == 'Network.requestWillBeSent'
        ]

    def get_cookies(self, as_dict: bool = False) -> Union[list[dict], dict[str, str]]:
        """
        Retrieves browser cookies.

        Args:
            as_dict: Return cookies as name-value dictionary if True

        Returns:
            Cookies as list of dicts or name-value dictionary
        """
        cookies: list[dict] = self.driver.get_cookies()

        if as_dict:
            # Convert to {name: value} dictionary
            return {cookie['name']: cookie['value'] for cookie in cookies}
        return cookies

    def get_cookie_header(self) -> str:
        """
        Formats cookies for HTTP Cookie header.

        Returns:
            Semicolon-separated cookie string
        """
        cookies: dict[str, str] = self.get_cookies(as_dict=True)  # type: ignore
        return "; ".join([f"{name}={value}" for name, value in cookies.items()])

    def get_local_storage(self) -> dict:
        """
        Retrieves contents of browser's local storage.

        Returns:
            Dictionary of local storage items
        """
        return self.driver.execute_script('return window.localStorage;')

    def __getattr__(self, name: str) -> Any:
        """
        Delegate undefined attributes to the underlying driver.

        Args:
            name: Attribute name to retrieve

        Returns:
            Requested attribute from the driver
        """
        return getattr(self.driver, name)

    def __enter__(self) -> uc.Chrome:
        """
        Enter context manager, returning the driver instance.

        Returns:
            Selenium Chrome driver instance
        """
        return self.driver

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit context manager, ensuring driver cleanup."""
        self.driver.quit()