import os

MARKER = """\
integration: Mark integration tests
unit: Mark unit tests
high: High Prioriry
medium: Medium Prioriry
low: Low Prioriry
"""

# fix error load dynaconf in pytest
os.environ["CATWB_TELEGRAM_TOKEN"] = "run_testing"
os.environ["CATWB_OPEN_WEATHER_TOKEN"] = "run_testing"


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)
