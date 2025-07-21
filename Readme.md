# Undetected Chrome WebDriver

[![Tests](https://github.com/a-ulianov/undetected-chrome-driver/actions/workflows/tests.yml/badge.svg)](https://github.com/a-ulianov/undetected-chrome-driver/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://github.com/a-ulianov/undetected-chrome-driver/actions/workflows/tests.yml)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

An enhanced Chrome WebDriver with anti-detection capabilities for web scraping and automation tasks, built on Selenium with additional stealth features.

## Features

- 🕵️‍♂️ **Anti-detection** techniques to bypass common bot detection systems
- 🌐 **Network monitoring** with performance logging capabilities
- 🍪 **Cookie management** with multiple output formats
- 💾 **LocalStorage access** for comprehensive data collection
- 🚀 **Headless mode** support with optimized default configurations
- 🔍 **Stealth configurations** via selenium-stealth integration
- ✅ **Fully tested** with comprehensive unit tests
- 📊 **Code coverage** tracking (100% coverage)

## Installation

### Prerequisites

- Python 3.11 or higher
- Chrome or Chromium browser installed

### Install via pip

```bash
pip install git+https://github.com/a-ulianov/undetected-chrome-driver
```

### Manual installation

1. Clone the repository:
   ```bash
   git clone https://github.com/a-ulianov/undetected-chrome-driver
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
from src.undetected_chrome_driver import UndetectedChromeDriver

# Custom configuration
driver = UndetectedChromeDriver(
    user_agent="Custom User Agent",
    chrome_driver_options=["--headless=new", "--window-size=1920,1080"],
    enable_performance_logging=True
)

with driver:
    # Navigate to a website
    driver.get('https://example.com')
    
    # Get all cookies as dictionary
    cookies = driver.get_cookies(as_dict=True)
    
    # Get network requests
    requests = driver.get_sent_requests()
    
    # Access local storage
    local_storage = driver.get_local_storage()
    
    # Get formatted cookie header
    cookie_header = driver.get_cookie_header()
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

- `get_sent_requests() -> List[dict]`: Returns network request logs
- `get_cookies(as_dict=False) -> Union[List[dict], dict]`: Returns cookies in specified format
- `get_cookie_header() -> str`: Returns cookies formatted for HTTP headers
- `get_local_storage() -> dict`: Returns browser's local storage contents

#### Context Manager

The driver supports context manager protocol for automatic cleanup:

```python
with UndetectedChromeDriver() as driver:
    # Your code here
# Driver automatically quits here
```

## Development

### Project Structure

```
your_project/
├── src/
│   ├── undetected_chrome_driver/
│   │   ├── __init__.py
│   │   ├── driver.py
│   │   └── logger.py
├── tests/
│   ├── conftest.py
│   └── test_driver.py
├── pyproject.toml
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

### CI/CD Pipeline

The project includes a GitHub Actions workflow (`.github/workflows/tests.yml`) that:
- Runs on push and pull requests
- Tests on Ubuntu with Python 3.11
- Generates coverage reports

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Selenium team for the base WebDriver implementation
- Undetected Chromedriver for anti-detection techniques
- Selenium Stealth for additional stealth configurations