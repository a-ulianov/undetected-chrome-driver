# Undetected Chrome WebDriver

[![Tests](https://github.com/a-ulianov/undetected-chrome-driver/actions/workflows/tests.yml/badge.svg)](https://github.com/a-ulianov/undetected-chrome-driver/actions/workflows/tests.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=a-ulianov_undetected-chrome-driver&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=a-ulianov_undetected-chrome-driver)
[![codecov](https://codecov.io/gh/a-ulianov/undetected-chrome-driver/branch/main/graph/badge.svg)](https://codecov.io/gh/a-ulianov/undetected-chrome-driver)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An enhanced Chrome WebDriver with anti-detection capabilities for web scraping and automation tasks, built on Selenium with additional stealth features.

## Features

- 🛡️ **Anti-detection** techniques to bypass common bot detection systems
- 🌐 **Network monitoring** with performance logging capabilities
- 🍪 **Cookie management** with multiple output formats
- 💾 **LocalStorage access** for comprehensive data collection
- 🖥️ **Headless mode** support with optimized default configurations
- 🕵️ **Stealth configurations** via selenium-stealth integration
- ✅ **Fully tested** with comprehensive unit tests (including logger tests)
- 📊 **Code coverage** tracking (100% coverage)
- ⚙️ **Config class** for centralized configuration management
- 🔄 **Object initialization** via `from_obj` method

## Installation

### Prerequisites

- Python 3.11 or higher
- Chrome or Chromium browser installed

### Install via pip

```bash
pip install git+https://github.com/a-ulianov/undetected-chrome-driver.git
```

### Manual installation

1. Clone the repository:
   ```bash
   git clone https://github.com/a-ulianov/undetected-chrome-driver.git
   cd undetected-chrome-driver
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

```python
from src.undetected_chrome_driver import UndetectedChromeDriver

with UndetectedChromeDriver() as driver:
    driver.get('https://example.com')
    print(driver.title)
```

### Advanced Usage

```python
from src.undetected_chrome_driver import UndetectedChromeDriver, Config

# Using Config class
config = Config()
driver = UndetectedChromeDriver.from_obj(config)

with driver:
    driver.get('https://example.com')
    
    # Access all features
    cookies = driver.get_cookies(as_dict=True)
    requests = driver.get_sent_requests()
    local_storage = driver.get_local_storage()
    cookie_header = driver.get_cookie_header()
```

### Logger Configuration

```python
from src.undetected_chrome_driver import Logger

# Custom logger setup
logger = Logger(
    logger_name="custom_logger",
    logging_level=logging.DEBUG,
    log_to_file=True,
    logs_dir="custom_logs",
    log_file="custom.log"
)
```

## API Documentation

### `UndetectedChromeDriver` Class

#### Constructor Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `user_agent` | str | Default UA string | Custom user agent string |
| `chrome_driver_options` | List[str] | Default options | Additional Chrome options |
| `enable_performance_logging` | bool | False | Enable network request logging |

#### Methods

- `from_obj(obj: Any) -> UndetectedChromeDriver`: Creates instance from object attributes
- `get_sent_requests() -> List[dict]`: Returns network request logs
- `get_cookies(as_dict=False) -> Union[List[dict], dict]`: Returns cookies in specified format
- `get_cookie_header() -> str`: Returns cookies formatted for HTTP headers
- `get_local_storage() -> dict`: Returns browser's local storage contents

### `Config` Class

Centralized configuration for driver settings including:
- User agent
- Chrome options
- Performance logging
- Logger configuration

### `Logger` Class

Customizable logger with:
- Console and file output
- Configurable logging levels
- Timestamp and format customization

## Development

### Project Structure

```
your_project/
├── src/
│   ├── undetected_chrome_driver/
│   │   ├── __init__.py
│   │   ├── driver.py
│   │   ├── logger.py
│   │   └── config.py
├── tests/
│   ├── conftest.py
│   ├── test_driver.py
│   └── test_logger.py
├── pyproject.toml
├── requirements.txt
└── main.py
```

### Running Tests

```bash
pytest tests/ --cov=src --cov-report=html
```

Or use the provided main script:

```bash
python main.py
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Selenium team for the base WebDriver implementation
- Undetected Chromedriver for anti-detection techniques
- Selenium Stealth for additional stealth configurations
