import pathlib

import pytest


@pytest.hookspec(firstresult=True)
def pytest_playwright_acquire_binaries(config: pytest.Config) -> pathlib.Path:  # noqa: ARG001
    """User defined behaviour for managing driver binaries.
    The default implementation of this hook is to acquire
    all binaries from the internet and store them as normal
    in the OS specific cache folders.

    This hook should return the path of the binaries directory.
    User defined invocations of this which do not return `None`
    will stop the call flow, overriding the default behaviour.

    :param config: The pytest.Config object (auto injected)
    """
