import sys
import pytest


def main() -> int:
    """Execute pytest with predefined configuration.

    This function runs pytest with the following default settings:
    - Looks for tests in the 'tests' directory
    - Stops after 3 failures (--maxfail=3)
    - Disables warning messages (--disable-warnings)
    - Uses quiet mode (-q) for less verbose output

    Returns:
        int: The exit code from pytest, which will be 0 if all tests passed,
             or 1 if any tests failed.
    """
    return pytest.main(["tests", "--maxfail=3", "--disable-warnings", "-q"])


if __name__ == "__main__":
    """Entry point when script is executed directly.

    Runs the test suite and exits with the appropriate status code.
    """
    exit_code = main()
    sys.exit(exit_code)