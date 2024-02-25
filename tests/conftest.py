pytest_plugins = ["pytester"]


import pytest


@pytest.hookimpl
def pytest_configure(config: pytest.Config) -> None:
    """Automatically download the playwright driver binaries
    for the execution.  Right now this acquires all binaries."""
    _ = config
