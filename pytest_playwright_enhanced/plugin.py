import typing

import pytest
from playwright import sync_api as pwsync

from .const import FixtureScopes
from .types import ContextKwargs


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
        "--pw-debug-",
        action="store_true",
        default=False,
        dest="pw_debug",
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
    parser.addoption(
        "--selenium-grid",
        action="store",
        default=None,
        dest="selenium_grid",
        help="The selenium grid endpoint to distribute tests remotely (experimental)",
    )


# The natural flow of playwright is to:
#   * Create a playwright object
#   * Launch a browser instance from that playwright object
#   * Launch a new browser context from that browser instance
#   * Launch a new (or multiple) page objects from the context.


@pytest.fixture(scope=FixtureScopes.Session)
def playwright() -> typing.Generator[pwsync.Playwright, None, None]:
    """Launch the core playwright context manager, at present only a
    synchronous path is supported however the plan is to add asynchronous
    support in future."""
    with pwsync.Playwright() as pw:
        yield pw


@pytest.fixture(scope=FixtureScopes.Function)
def browser_type(playwright: pwsync.Playwright) -> pwsync.BrowserType:
    """Dynamically fetch the browser type for this specific test."""
    return getattr(playwright, "browser")


@pytest.fixture(scope=FixtureScopes.Session)
def browser(
    browser_arguments: ContextKwargs,
    dynamic_browser_fn: typing.Callable[[], pwsync.Browser],
) -> typing.Generator[pwsync.Browser, None, None]:
    """Yields the core browser instance."""
    browser = dynamic_browser_fn(**browser_arguments)
    yield browser
    browser.close()


@pytest.fixture(scope=FixtureScopes.Session)
def browser_arguments() -> ContextKwargs:
    """The configuration to launching browser arguments.  Override this fixture to pass arbitrary
    arguments to the launched Browser instance."""
    return {}


@pytest.fixture(scope=FixtureScopes.Function)
def context_arguments() -> ContextKwargs:
    """The configuration to launching contexts.  Override this fixture to pass arbitrary
    arguments to the launched Context instance."""
    return {}


@pytest.fixture
def page(
    pytestconfig: pytest.Config,
    context: pwsync.BrowserContext,
) -> typing.Generator[pwsync.Page, None, None]:
    """Launch a new page (tab) as a child of the browser context."""
    # Todo: Allow per page **kwargs
    page = context.new_page()
    base_url = pytestconfig.option.base_url
    if base_url is not None:
        page.goto(base_url)
    yield page
    page.close()


@pytest.fixture(scope=FixtureScopes.Function)
def context(
    browser: pwsync.Browser,
    context_arguments: ContextKwargs,
) -> typing.Generator[pwsync.BrowserContext, None, None]:
    """A scope session scoped browser context."""
    context = browser.new_context(**context_arguments)
    yield context
    context.close()


# ----- Hook Specifics

PhaseReportKey = pytest.StashKey[typing.Dict[str, pytest.CollectReport]]()


@pytest.hookimpl(wrapper=True, tryfirst=True)
def pytest_runtest_makereport(
    item: pytest.Item,
) -> typing.Generator[None, None, pytest.CollectReport]:
    """A hook implementation to determine if a test passed.
    Fixtures can fetch this information later (post-yield)
    by inspecting the request.node.stash with the PhaseReportKey.
    """
    report = yield
    item.stash.setdefault(PhaseReportKey, {})[report.when] = report
    return report
