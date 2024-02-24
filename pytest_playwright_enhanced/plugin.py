import typing

import pytest
from playwright import sync_api as pwsync

from .const import FixtureScopes


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register argparse-style options and ini-style configuration values
    for the plugin."""
    parser.addoption(
        "--headed",
        action="store_true",
        default=False,
        dest="headed",
        help="Should tests be ran in headed mode, defaults to headless.",
    )
    parser.addoption(
        "--root-url",
        action="store",
        default=None,
        dest="root_url",
        help="The root url that should be visited when launching a page.",
    )
    parser.addoption(
        "--browser",
        action="append",
        default=[],
        type=list,
        dest="browser",
        help="The browser engine to use.",
        choices=["chromium", "webkit", "firefox"],
    )
    parser.addoption(
        "--emulate",
        action="store",
        dest="emulate",
        help="The device to be emulated.",
    )
    parser.addoption(
        "--throttle",
        action="store",
        dest="throttle",
        type=float,
        help="Add arbitrary delay between playwright actions.",
    )
    parser.addoption(
        "--debug",
        action="store_true",
        default=False,
        dest="debug",
        help="Allow debugging by forcing `PWDEBUG=console`.",
    )

    parser.addoption(
        "--artifacts",
        action="store",
        default="test-artifacts",
        dest="test-artifacts",
        help="The folder name where various artifacts are stored",
    )

    parser.addoption(
        "--screenshot-on-fail",
        action="store_false",
        default=True,
        dest="screenshot_on_fail",
        help="Retain captured screenshots in the artifacts directory if a test fails.",
    )
    parser.addoption(
        "--video-on-fail",
        action="store_false",
        default=True,
        dest="video_on_fail",
        help="Retain captured videos in the artifacts directory if a test fails.",
    )
    parser.addoption(
        "--trace-on-fail",
        action="store_false",
        default=True,
        dest="trace_on_fail",
        help="Retain captured trace in the artifacts directory if a test fails.",
    )


@pytest.fixture(scope=FixtureScopes.Session)
def playwright() -> typing.Generator[pwsync.Playwright, None, None]:
    with pwsync.Playwright() as pw:
        yield pw


@pytest.fixture(scope=FixtureScopes.Function)
def browser_type(playwright: pwsync.Playwright) -> pwsync.BrowserType:
    """Dynamically fetch the browser type for this specific test."""
    return getattr(playwright, "browser")


@pytest.fixture(scope=FixtureScopes.Session)
def browser(
    browser_type: pwsync.BrowserType, callable: typing.Callable[[], pwsync.Browser]
) -> typing.Generator[pwsync.Browser, None, None]:
    """Yields the core browser instance."""


@pytest.fixture(scope=FixtureScopes.Session)
def browser_arguments() -> dict[str, str]:
    """The configuration to launching browser arguments.  Override this fixture to pass arbitrary
    arguments to the launched Browser instance."""


@pytest.fixture
def page(context: pwsync.BrowserContext) -> pwsync.Page:
    """A fresh page instance between tests."""
    return context.new_page()


@pytest.fixture(scope=FixtureScopes.Function)
def context() -> pwsync.BrowserContext:
    """A scope session scoped browser context."""
