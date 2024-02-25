import pytest


def pytest_playwright_acquire_binaries(config: pytest.Config) -> None:  # noqa: ARG001
    """User defined behaviour for managing driver binaries.
    The default implementation of this hook is to acquire
    all binaries from the internet and store them as normal
    in the OS specific cache folders.
    """
