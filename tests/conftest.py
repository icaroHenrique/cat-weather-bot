MARKER = """\
integration: Mark integration tests
unit: Mark unit tests
high: High Prioriry
medium: Medium Prioriry
low: Low Prioriry
"""


def pytest_configure(config):
    for line in MARKER.split("\n"):
        config.addinivalue_line("markers", line)
