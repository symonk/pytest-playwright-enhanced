from playwright.sync_api import Browser
from playwright.sync_api import Playwright

from .types import AnyDict


def chromium_browser_strategy(pw: Playwright, launch_kw: AnyDict) -> Browser:
    """Launch a chromium browser instance.

    :param pw: The sync playwright instance."""
    return pw.chromium.launch(**launch_kw)


def firefox_browser_strategy(pw: Playwright, launch_kw: AnyDict) -> Browser:
    """Launch a firefox browser instance.

    :param pw: The sync playwright instance."""
    return pw.firefox.launch(**launch_kw)


def webkit_browser_strategy(pw: Playwright, launch_kw: AnyDict) -> Browser:
    """Launch a webkit browser instance.

    :param pw: The sync playwright instance."""
    return pw.webkit.launch(**launch_kw)


BROWSER_FACTORY = {
    "chromium": chromium_browser_strategy,
    "firefox": firefox_browser_strategy,
    "webkit": webkit_browser_strategy,
}
