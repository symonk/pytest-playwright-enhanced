from __future__ import annotations

import os
from typing import Any

import pytest


def register_env_defer(var: str, val: str, config: pytest.Config) -> None:
    """Register an environment variable and a clean up call back
    to remove it at the end of the run.

    :param var: The environment variable (key).
    :param val: The environment value.
    :param config: The pytest config object to register the callback with.
    """
    os.environ[var] = val

    # This should never raise; no default as it's a bug if it does! (for now)
    def defer(var: str) -> None:
        os.environ.pop(var)

    callback = lambda: defer(var)
    config.add_cleanup(callback)


def safe_to_run_plugin(config: pytest.Config) -> bool:
    """Return whether it is safe to execute plugin code, otherwise
    the plugin should be avoided to prevent unnecessary side effects."""
    if config.option.help:
        return False
    if config.option.showfixtures:
        return False
    if config.option.collectonly:
        return False
    return True


def parse_browser_kwargs_from_node(
    item: pytest.Item, default: dict[str, Any]
) -> dict[str, Any]:
    """Given a test node item, return the parsed marker
    overrides specified for the playwright `Browser` instance.

    :param item: The `pytest.Item` for the executing test.
    """
    browser_kwargs = item.get_closest_marker("browser_kwargs")
    if browser_kwargs is None:
        return default
    return browser_kwargs.kwargs.get("config", default)
