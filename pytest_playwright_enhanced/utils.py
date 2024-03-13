from __future__ import annotations

import os
from typing import Any

import pytest

from .launch_kwargs_strategy import STRATEGY_FACTORY


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


def resolve_commandline_arg_defaults(
    config: pytest.Config, engine: str
) -> dict[str, Any]:
    """Given the pytest config, returns a dictionary mapping the defaults
    that can be shovelled directly into the playwright browser launch method.

    :param config: The `pytest.Config` object.
    :param engine: The browser engine to return options for.

    Some options are engine specific, these are automatically filtered out.
    """
    defaults = {}
    if (exec_path := config.option.executable_path) is not None:
        defaults["executable_path"] = exec_path
    if (channel := config.option.browser_channel) is not None:
        defaults["channel"] = channel
    defaults["timeout"] = config.option.browser_timeout
    if config.option.headed:
        defaults["headless"] = False
    if config.option.chromium_sandbox:
        defaults["chromium_sandbox"] = True

    # Todo: Sort the traces & download dir options.
    # devtools we will NOT offer
    # Todo: sort proxy option
    # download path we will bake into the plugin

    # These are not configurable options, but enforced by the plugin
    defaults["handle_sighup"] = True
    defaults["handle_sigint"] = True
    defaults["handle_sigterm"] = True
    return STRATEGY_FACTORY[engine](defaults)
