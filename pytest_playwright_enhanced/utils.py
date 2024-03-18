from __future__ import annotations

import os
from typing import Any

import pytest

from .exceptions import PWEMarkerError
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
    :param default: A mapping to return if the marker cannot be found on the test.
    """
    parsed = _check_for_marker(item, "browser_kwargs")
    return parsed or default


def parse_context_kwargs_from_node(
    item: pytest.Item, default: dict[str, Any]
) -> dict[str, Any]:
    """Given a test node item, return the parsed marker overrides specified
    for the playwright `Context` instance.

    :param item: The `pytest.Item` for the executing test.
    :param default: A mapping to return if the marker cannot be found on the test.
    """
    parsed = _check_for_marker(item, "context_kwargs")
    return parsed or default


def _check_for_marker(item: pytest.Item, marker_name: str) -> dict[str, Any]:
    """Attempt to parse a browser or context marker to grab the user defied
    keyword args."""
    marker = item.get_closest_marker(marker_name)
    if marker is None:
        return {}
    if marker.args:
        raise PWEMarkerError(marker.args, marker_name, item.name)
    # Allow a callback function to be returned to merge into the marker kwargs
    callback = marker.kwargs.get("callback")
    if callback is not None:
        return {**marker.kwargs, **callback(item)}
    return marker.kwargs


def resolve_browser_cli_flag_defaults(
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


def resolve_context_cli_flag_defaults(config: pytest.Config) -> None:
    """Parses context-specific options from the global command line
    options.

    These options are then merged with test specific overrides for the context
    and lastly any dynamic options provided via callback= take utmost priority.

    :param config: The `pytest.Config` object.
    """
    defaults = {}
    if (base_url := config.option.base_url) is not None:
        defaults["base_url"] = base_url
    return defaults


def is_master_worker(config: pytest.Config) -> bool:
    """Detect if the calling code is an xdist worker
    or the master worker."""
    return not hasattr(config, "workerinput")


def test_was_not_skipped_and_passed(item: pytest.Item, key: pytest.StashKey) -> bool:
    """Returns a boolean if the test item
    was an actual phase in the call phase.

    :param item: The test item.
    :param key: The stash key for tracking status.

    Note: This should only be called from a `post-yield` fixture."""
    report = item.stash[key]
    setup_ok = "setup" in report and not report["setup"].failed
    call_ok = "call" in report and not report["call"].failed
    return setup_ok and call_ok
