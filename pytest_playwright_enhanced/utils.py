import os

import pytest


def register_env_defer(var: str, val: str, config: pytest.Config) -> None:
    """Register an environment variable and a clean up call back
    to remove it at the end of the run.

    :param var: The environment variable (key).
    :param val: The environment value.
    :param config: The pytest config object to register the callback with.
    """
    os.environ[var] = val
    callback = lambda: os.environ.pop(var)
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
