from __future__ import annotations

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

    :param config: The pytest.Config object (auto injected) by pluggy.
    """


@pytest.hookspec(firstresult=True)
def pytest_playwright_is_debugging(config: pytest.Config) -> bool:  # noqa: ARG001
    """Allow users to define custom debugging detection.  By default
    `pytest-playwright-enhanced` will detect VSCode, but alternative
    implementations  can be used here.

    :param config: The pytest.Config object (auto injected) by pluggy."""


@pytest.hookspec(firstresult=True)
def pytest_playwright_browser_env(config: pytest.Config) -> dict[str, str]:  # noqa: ARG001
    """Allows user defined code to control the environment variables passed
    on when launching the browser instance.  This should return a dictionary
    of env vars.  The default is the process.env"""
