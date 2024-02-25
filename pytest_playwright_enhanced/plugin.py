import typing

import pytest
from playwright import sync_api as pwsync

from .const import BrowserEngine
from .const import FixtureScope
from .types import ContextKwargs


def pytest_addoption(parser: pytest.Parser) -> None:
    """Register argparse-style options and ini-style configuration values
    for the plugin.
    """
    pwe = parser.getgroup("playwright-enhanced")
    pwe.addoption(
        "--headed",
        action="store_true",
        default=False,
        dest="headed",
        help="Should tests be ran in headed mode, defaults to headless.",
    )
    pwe.addoption(
        "--root-url",
        action="store",
        default=None,
        dest="root_url",
        help="The root url that should be visited when launching a page.",
    )
    pwe.addoption(
        # Todo, allow choices in future.
        "--browser",
        action="store",
        default="chromium",
        dest="browser",
        help="The browser engine to use.",
    )
    pwe.addoption(
        "--emulate",
        action="store",
        dest="emulate",
        help="The device to be emulated.",
    )
    pwe.addoption(
        "--throttle",
        action="store",
        dest="throttle",
        type=float,
        help="Add arbitrary delay between playwright actions.",
    )
    pwe.addoption(
        "--pw-debug-",
        action="store_true",
        default=False,
        dest="pw_debug",
        help="Allow debugging by forcing `PWDEBUG=console`.",
    )

    pwe.addoption(
        "--artifacts",
        action="store",
        default="test-artifacts",
        dest="test-artifacts",
        help="The folder name where various artifacts are stored",
    )

    pwe.addoption(
        "--screenshot-on-fail",
        action="store_false",
        default=True,
        dest="screenshot_on_fail",
        help="Retain captured screenshots in the artifacts directory if a test fails.",
    )
    pwe.addoption(
        "--video-on-fail",
        action="store_false",
        default=True,
        dest="video_on_fail",
        help="Retain captured videos in the artifacts directory if a test fails.",
    )
    pwe.addoption(
        "--trace-on-fail",
        action="store_false",
        default=True,
        dest="trace_on_fail",
        help="Retain captured trace in the artifacts directory if a test fails.",
    )
    pwe.addoption(
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


@pytest.fixture(scope=FixtureScope.Session)
def playwright() -> typing.Generator[pwsync.Playwright, None, None]:
    """Launch the core playwright context manager, at present only a
    synchronous path is supported however the plan is to add asynchronous
    support in future.
    """
    with pwsync.sync_playwright() as pw:
        yield pw


@pytest.fixture(scope=FixtureScope.Function)
def browser_engine(pytestconfig: pytest.Config) -> str:
    """Returns the type of browser that will be used."""
    return pytestconfig.option.browser


@pytest.fixture(scope=FixtureScope.Function)
def is_chromium(browser_engine: str) -> bool:
    """Returns true if the running tests will be executed
    on a chromium based browser.

    :param browser_type: The command line flag value for --browser.
    """
    return browser_engine.lower() == BrowserEngine.CHROMIUM


@pytest.fixture(scope=FixtureScope.Function)
def is_webkit(browser_engine: str) -> bool:
    """Returns true if the running tests will be executed
    on a webkit based browser.

    :param browser_type: The command line flag value for --browser.
    """
    return browser_engine.lower() == BrowserEngine.WEBKIT


@pytest.fixture(scope=FixtureScope.Function)
def is_firefox(browser_engine: str) -> bool:
    """Returns true if the running tests will be executed
    on a firefox based browser.

    :param browser_type: The command line flag value for --browser.
    """
    return browser_engine.lower() == BrowserEngine.FIREFOX


@pytest.fixture(scope=FixtureScope.Session)
def root_url(pytestconfig: pytest.Config) -> str:
    """Returns the root url. If provided pages will automatically
    attempt to load this url after creation."""
    return pytestconfig.option.root_url


@pytest.fixture(scope=FixtureScope.Session)
def browser(
    request: pytest.FixtureRequest,
    playwright: pwsync.Playwright,
    browser_arguments: ContextKwargs,
) -> typing.Generator[pwsync.Browser, None, None]:
    """Yields the core browser instance."""
    browser = getattr(playwright, request.config.option.browser).launch(
        **browser_arguments,
    )
    yield browser
    browser.close()


@pytest.fixture(scope=FixtureScope.Session)
def browser_arguments() -> ContextKwargs:
    """The configuration to launching browser arguments.  Override this fixture to pass arbitrary
    arguments to the launched Browser instance.
    """
    return {}


@pytest.fixture(scope=FixtureScope.Function)
def context_arguments() -> ContextKwargs:
    """The configuration to launching contexts.  Override this fixture to pass arbitrary
    arguments to the launched Context instance.
    """
    return {}


@pytest.fixture(scope=FixtureScope.Function)
def page(
    pytestconfig: pytest.Config,
    context: pwsync.BrowserContext,
) -> typing.Generator[pwsync.Page, None, None]:
    """Launch a new page (tab) as a child of the browser context."""
    page = context.new_page()
    base_url = pytestconfig.option.base_url
    if base_url is not None:
        page.goto(base_url)
    yield page
    page.close()


@pytest.fixture(scope=FixtureScope.Function)
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
