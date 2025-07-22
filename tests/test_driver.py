import json
import pytest
from unittest.mock import MagicMock, patch
# noinspection PyUnresolvedReferences
from undetected_chrome_driver import UndetectedChromeDriver

# Mock constants for testing
MOCK_USER_AGENT = "Mozilla/5.0 (Test Agent)"
TEST_URL = "https://example.com"


@pytest.fixture
def mock_driver():
    """Fixture to mock the Chrome driver and its dependencies."""
    with patch('undetected_chromedriver.Chrome') as mock_chrome, \
            patch('webdriver_manager.chrome.ChromeDriverManager') as mock_manager, \
            patch('selenium_stealth.stealth'):
        # Setup mock driver
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_manager.return_value.install.return_value = "/mock/path/chromedriver"

        # Mock driver methods
        mock_driver.get_log.return_value = []
        mock_driver.get_cookies.return_value = [{"name": "test", "value": "cookie"}]
        mock_driver.execute_script.return_value = {"key": "value"}

        yield mock_driver


def test_driver_initialization_defaults(mock_driver):
    """Test driver initialization with default parameters."""
    driver = UndetectedChromeDriver()

    with driver:
        # Verify default options applied
        assert driver.user_agent == UndetectedChromeDriver._user_agent
        assert not driver._is_performance_logging_enabled


def test_custom_initialization(mock_driver):
    """Test driver initialization with custom parameters."""
    custom_options = ["--custom-option"]
    driver = UndetectedChromeDriver(
        user_agent=MOCK_USER_AGENT,
        chrome_driver_options=custom_options,
        enable_performance_logging=True
    )

    with driver:
        # Verify custom parameters
        assert driver.user_agent == MOCK_USER_AGENT
        assert driver._is_performance_logging_enabled


def test_get_sent_requests(mock_driver):
    """Test network request retrieval functionality."""
    # Setup performance logs
    mock_logs = [
        {"message": json.dumps({"message": {"method": "Network.requestWillBeSent"}})},
        {"message": json.dumps({"message": {"method": "Other.method"}})}
    ]
    mock_driver.get_log.return_value = mock_logs

    driver = UndetectedChromeDriver(enable_performance_logging=True)
    with driver:
        requests = driver.get_sent_requests()

        assert len(requests) == 1
        assert requests[0]["message"] == mock_logs[0]["message"]


def test_get_sent_requests_disabled(mock_driver, caplog):
    """Test warning when performance logging is disabled."""
    driver = UndetectedChromeDriver(enable_performance_logging=False)

    with driver:
        requests = driver.get_sent_requests()

        assert len(requests) == 0
        assert "Performance logging is disabled" in caplog.text


def test_cookie_retrieval(mock_driver):
    """Test cookie retrieval formats."""
    driver = UndetectedChromeDriver()
    with driver:
        # Test list format
        cookies_list = driver.get_cookies()
        assert isinstance(cookies_list, list)
        assert cookies_list[0]["name"] == "test"

        # Test dictionary format
        cookies_dict = driver.get_cookies(as_dict=True)
        assert isinstance(cookies_dict, dict)
        assert cookies_dict["test"] == "cookie"


def test_cookie_header_generation(mock_driver):
    """Test proper cookie header formatting."""
    driver = UndetectedChromeDriver()
    with driver:
        header = driver.get_cookie_header()
        assert header == "test=cookie"


def test_local_storage_retrieval(mock_driver):
    """Test local storage retrieval."""
    driver = UndetectedChromeDriver()
    with driver:
        storage = driver.get_local_storage()
        assert storage == {"key": "value"}
        mock_driver.execute_script.assert_called_with('return window.localStorage;')


def test_context_manager(mock_driver):
    """Test context manager functionality."""
    driver = UndetectedChromeDriver()
    with driver:
        driver.get(TEST_URL)
        mock_driver.get.assert_called_once_with(TEST_URL)

    mock_driver.quit.assert_called_once()


def test_attribute_delegation(mock_driver):
    """Test attribute delegation to underlying driver."""
    driver = UndetectedChromeDriver()
    with driver:
        # Set a mock value for the title property
        mock_driver.title = "Test Page"

        # Access property
        result = driver.title

        # Verify we got the mock value
        assert result == "Test Page"

def test_stealth_configuration(mock_driver):
    """Test stealth configuration is applied."""
    with patch('selenium_stealth.stealth') as mock_stealth:
        driver = UndetectedChromeDriver()
        with driver:
            mock_stealth.assert_called_once_with(
                driver.driver,
                languages=['en-US', 'en'],
                user_agent=driver.user_agent,
                vendor='Google Inc.',
                platform='Win64',
                webgl_vendor='Intel Inc.',
                renderer='Intel Iris OpenGL Engine',
                fix_hairline=True
            )

def test_capabilities_configuration(mock_driver):
    """Test performance logging capabilities setup."""
    driver = UndetectedChromeDriver(enable_performance_logging=True)
    with driver:
        assert 'goog:loggingPrefs' in driver.capabilities
        assert driver.capabilities['goog:loggingPrefs'] == {'performance': 'ALL'}


def test_from_obj_method(mock_driver):
    """Test the from_obj class method for creating driver instances from objects."""

    # Create a mock object with attributes and methods
    class MockConfig:
        def __init__(self):
            self.user_agent = "Custom User Agent"
            self.chrome_driver_options = ["--custom-option"]
            self.enable_performance_logging = True
            self.logger_name = "test_logger"

    mock_config = MockConfig()

    # Test the from_obj method
    with patch.object(UndetectedChromeDriver, '__init__', return_value=None) as mock_init:
        UndetectedChromeDriver.from_obj(mock_config)

        # Verify __init__ was called with the correct arguments
        mock_init.assert_called_once_with(
            user_agent=mock_config.user_agent,
            chrome_driver_options=mock_config.chrome_driver_options,
            enable_performance_logging=mock_config.enable_performance_logging,
            logger_name=mock_config.logger_name
        )
