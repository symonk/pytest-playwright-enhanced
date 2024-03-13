from __future__ import annotations

from .const import BrowserEngine


def chromium_launch_strategy(defaults: dict[str, str]) -> ...:
    """Strategy function for removing overrides that are not applicable
    to chromium when building launch arguments."""
    return defaults


def firefox_launch_strategy(defaults: dict[str, str]) -> ...:
    """Strategy function for removing overrides that are not applicable
    to firefox when building launch arguments."""
    defaults.pop("chromium_sandbox", None)
    return defaults


def webkit_launch_strategy(defaults: dict[str, str]) -> ...:
    """Strategy function for removing overrides that are not applicable
    to webkit when building launch arguments."""
    defaults.pop("chromium_sandbox", None)
    return defaults


STRATEGY_FACTORY = {
    BrowserEngine.CHROMIUM: chromium_launch_strategy,
    BrowserEngine.FIREFOX: firefox_launch_strategy,
    BrowserEngine.WEBKIT: webkit_launch_strategy,
}
