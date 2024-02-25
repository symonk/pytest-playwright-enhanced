import os
import pathlib
import subprocess
import typing

import pytest
from playwright import sync_api as pwsync

from .const import BrowserEngine
from .const import EnvironmentVars
from .const import FixtureScope
from .types import ContextKwargs


@pytest.hookimpl
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
        choices=(BrowserEngine.CHROMIUM, BrowserEngine.WEBKIT, BrowserEngine.FIREFOX),
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
        "--pw-debug",
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
    pwe.addoption(
        "--download-host",
        action="store",
        default=None,
        dest="driver_download_host",
        help="The download for binaries, such as an internal artifact repository.",
    )
    pwe.addoption(
        "--drivers-path",
        action="store",
        default=None,
        dest="driver_path",
        help="The download path where playwright downloads should store browser binaries.",
    )
    pwe.addoption(
        "--acquire-drivers",
        action="store_true",
        default=False,
        dest="acquire_drivers",
        help="Should `pytest-playwright-enhanced` automatically download drivers at runtime for the matching markers.",
    )


@pytest.hookimpl
def pytest_configure(config: pytest.Config) -> None:
    """Register plugin specific markers for functionality.
    pytest-playwright-enhanced specific hook functionality is
    registered and invoked as part of the `pytest_configure`
    workflow.

    :param config: The pytest `Config` object. (auto injected by pluggy).
    """
    config.addinivalue_line(
        "markers",
        "page_kwargs: provide additional arguments for new playwright pages",
    )
    config.addinivalue_line(
        "markers",
        "context_kwargs: provide additional arguments for new playwright contexts",
    )
    # conditionally invoke the acquire binaries hook.
    if config.option.acquire_drivers:
        _ = config.hook.pytest_playwright_acquire_binaries(config=config)

    # conditionally enable console debugging.
    if config.option.pw_debug:
        os.environ[EnvironmentVars.PWDEBUG] = "console"
        config.add_cleanup(lambda: os.environ.pop(EnvironmentVars.PWDEBUG))

    if driver_download_host := config.option.driver_download_host is not None:
        os.environ[EnvironmentVars.PLAYWRIGHT_DOWNLOAD_HOST] = driver_download_host
        config.add_cleanup(
            lambda: os.environ.pop(EnvironmentVars.PLAYWRIGHT_DOWNLOAD_HOST)
        )

    if driver_path := config.option.driver_path is not None:
        os.environ[EnvironmentVars.PLAYWRIGHT_BROWSERS_PATH] = driver_path
        config.add_cleanup(
            lambda: os.environ.pop(EnvironmentVars.PLAYWRIGHT_BROWSERS_PATH)
        )


@pytest.hookimpl
def pytest_addhooks(pluginmanager: pytest.PytestPluginManager) -> None:
    """Register new `playwright-pytest-enhanced` specific hooking
    functionality."""
    from pytest_playwright_enhanced import hooks as playwright_hooks

    pluginmanager.add_hookspecs(playwright_hooks)


@pytest.hookimpl(trylast=True)
def pytest_playwright_acquire_binaries(config: pytest.Config) -> None:
    """The default implementation for binary acquisition.

    :param config: The `pytest.Config` object. (auto injected).

    # Todo: This is a dummy implementation and needs some love.
    """
    print("DOWNLOADED BINARIES")
    _ = config
    return None
    completed_process = subprocess.run(
        ["playwright", "install"],
        capture_output=True,
        check=False,
    )
    if completed_process.returncode:
        raise pytest.UsageError("Problem downloading playwright driver binaries!")
    return pathlib.Path()


@pytest.fixture(scope=FixtureScope.Function)
def playwright() -> typing.Generator[pwsync.Playwright, None, None]:
    """Launch the core playwright context manager, at present only a
    synchronous path is supported however the plan is to add asynchronous
    support in future.
    """
    with pwsync.sync_playwright() as pw:
        yield pw


@pytest.fixture(scope=FixtureScope.Session)
def is_debugging(pytestconfig: pytest.Config) -> bool:
    """Returns if the execution is running with PWDEBUG enabled."""
    return pytestconfig.option.pw_debug


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


@pytest.fixture(scope=FixtureScope.Function)
def root_url(pytestconfig: pytest.Config) -> str:
    """Returns the root url. If provided pages will automatically
    attempt to load this url after creation."""
    return pytestconfig.option.root_url


@pytest.fixture(scope=FixtureScope.Function)
def browser(
    browser_engine: str,
    playwright: pwsync.Playwright,
    browser_arguments: ContextKwargs,
) -> typing.Generator[pwsync.Browser, None, None]:
    """Yields the core browser instance."""
    browser = getattr(playwright, browser_engine).launch(
        **browser_arguments,
    )
    yield browser
    browser.close()


@pytest.fixture(scope=FixtureScope.Function)
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
