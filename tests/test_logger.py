"""Tests for Logger class."""

import logging
import os
import pytest
# noinspection PyUnresolvedReferences
from undetected_chrome_driver import Logger


class TestLogger:
    """Test class for verifying the functionality of the Logger class."""

    def test_default_initialization(self):
        """Verify default initialization creates a logger with console handler only."""
        logger_name = "test_default_logger"
        logger = Logger(logger_name=logger_name)

        assert logger.logger.name == logger_name
        assert logger.logger.level == logging.INFO
        assert len(logger.logger.handlers) == 1
        assert isinstance(logger.logger.handlers[0], logging.StreamHandler)

    def test_file_logging_initialization(self, tmp_path):
        """Verify file handler is added when log_to_file is enabled."""
        logs_dir = tmp_path / "logs"
        log_file = "test.log"
        logger = Logger(
            logger_name="test_file_logger",
            log_to_file=True,
            logs_dir=str(logs_dir),
            log_file=log_file
        )

        assert len(logger.logger.handlers) == 2

        file_handler = logger.logger.handlers[1]
        assert isinstance(file_handler, logging.FileHandler)
        assert file_handler.level == logging.INFO
        assert os.path.exists(logs_dir / log_file)

    def test_invalid_file_parameters(self):
        """Verify ValueError is raised for invalid file logging parameters."""
        with pytest.raises(ValueError):
            Logger(log_to_file=True, logs_dir=None, log_file="valid.log")

        with pytest.raises(ValueError):
            Logger(log_to_file=True, logs_dir="valid_dir", log_file="")

    def test_log_output_format(self, caplog):
        """Verify log messages use the correct format."""
        logger_name = "test_format_logger"
        logger = Logger(logger_name=logger_name)
        test_message = "Test log message"

        # Capture logs at INFO level
        with caplog.at_level(logging.INFO, logger=logger_name):
            logger.logger.info(test_message)

        # Get formatted log output
        log_output = caplog.text.strip()

        assert logger_name in log_output
        assert test_message in log_output
