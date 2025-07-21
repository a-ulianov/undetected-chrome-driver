import pytest

# Configure logging for tests
@pytest.fixture(autouse=True)
def setup_logging(caplog):
    caplog.set_level("INFO")