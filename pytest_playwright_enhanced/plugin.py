from __future__ import annotations

import os
import pathlib
import subprocess
import sys
import typing

import pytest
from playwright import sync_api as pwsync
from playwright._impl._driver import get_driver_env

from .browser_strategy import BROWSER_FACTORY
from .const import BrowserEngine
from .const import EnvironmentVars
from .const import FixtureScope
from .types import ContextKwargs
from .utils import parse_browser_kwargs_from_node
from .utils import register_env_defer
from .utils import resolve_commandline_arg_defaults
from .utils import safe_to_run_plugin


@pytest.hookimpl
def pytest_addoption(parser: pytest.Parser) -> None:
    """Register argparse-style options and ini-style configuration values
    for the plugin.
    """
    pwe = parser.getgroup(
        "playwright-enhanced",
        "Batteries included playwright for pytest",
    )
    pwe.addoption(
        "--headed",
        action="store_true",
        default=False,
        dest="headed",
        help="Should tests be ran headed. (Defaults to headless).",
    )
    pwe.addoption(
        "--root-url",
        action="store",
        default=None,
        dest="root_url",
        help="The base_url that is loaded by pages. (Defaults to None).",
    )
    pwe.addoption(
        "--browser",
        action="append",
        default=[],
        dest="browser",
        choices=(BrowserEngine.CHROMIUM, BrowserEngine.WEBKIT, BrowserEngine.FIREFOX),
        help="The browsers to run all tests against.  Defaults to only chromium",
    )
    pwe.addoption(
        "--device",
        action="store",
        dest="device",
        help="The device to be emulated.",
    )
    pwe.addoption(
        "--slow-mo",
        action="store",
        dest="slow_mo",
        type=int,
        default=0,
        help="Add arbitrary delay between playwright actions.",
    )
    pwe.addoption(
        "--pw-debug",
        action="store_true",
        default=False,
        dest="pw_debug",
        help="Allow debugging by forcing `PWDEBUG=console`.",
    )

    # Todo: Each test run should store all artifacts in a shared temp directory?
    # Todo: By design, downloaded artifacts are destroyed when a browser ctx is closed.
    pwe.addoption(
        "--artifacts",
        action="store",
        default="playwright-enhanced-results",
        dest="test-artifacts",
        help="The folder name where various artifacts are stored",
    )

    pwe.addoption(
        "--screenshot-on-fail",
        action="store_true",
        default=False,
        dest="screenshot_on_fail",
        help="Retain captured screenshots in the artifacts directory if a test fails.",
    )
    pwe.addoption(
        "--video-on-fail",
        action="store_true",
        default=False,
        dest="video_on_fail",
        help="Retain captured videos in the artifacts directory if a test fails.",
    )
    pwe.addoption(
        "--trace-on-fail",
        action="store_true",
        default=False,
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
        action="store",
        default="no",
        dest="acquire_drivers",
        choices=("yes", "no", "with-deps"),
        help="Should playwright enhanced auto acquire driver binaries.",
    )
    pwe.addoption(
        "--executable-path",
        action="store",
        default=None,
        dest="executable_path",
        help=(
            "[Risky] Use this path for browser executables (not the bundled playwright ones).  Use at your own risk as \n\n"
            "playwright only really supports the bundled options.  This is experimental."
        ),
    )
    pwe.addoption(
        "--channel",
        action="store",
        dest="browser_channel",
        default=None,
        choices=(
            "chrome",
            "chrome-beta",
            "chrome-dev",
            "chrome-canary",
            "msedge",
            "msedge-beta",
            "msedge-dev",
            "msedge-canary",
        ),
        help="The browser distribution channel to use.",
    )
    pwe.addoption(
        "--browser-timeout",
        action="store",
        dest="browser_timeout",
        type=int,
        default=30_000,
        help=(
            "The default timeout in milliseconds for the browser instance to launch. \n\n"
            "Set to `0` to completely disable.  30 seconds by default."
        ),
    )
    pwe.addoption(
        "--chromium-sandbox",
        action="store_true",
        default=False,
        dest="chromium_sandbox",
        help="Enable chromium sandboxing for chromium engine only.  defaults Off.",
    )
    # Todo: Proxy settings?


@pytest.hookimpl
def pytest_configure(config: pytest.Config) -> None:
    """Register plugin specific markers for functionality.
    pytest-playwright-enhanced specific hook functionality is
    registered and invoked as part of the `pytest_configure`
    workflow.

    :param config: The pytest `Config` object. (auto injected by pluggy).
    """

    # skip this plugin entirely when performing collection.
    if not safe_to_run_plugin(config):
        return

    # Avoid spurious warnings by registering plugin specific markers.
    config.addinivalue_line(
        "markers", "pw_only_on_browsers(name): Opt in browsers to iterate a test on."
    )
    config.addinivalue_line(
        "markers",
        "context_kwargs: provide additional arguments for new playwright contexts.",
    )
    config.addinivalue_line(
        "markers",
        "browser_kwargs: provide additional arguments for new playwright browsers.",
    )
    # conditionally invoke the acquire binaries hook.
    if config.option.acquire_drivers != "no":
        _ = config.hook.pytest_playwright_acquire_binaries(config=config)
    prepare_environment(config)


def prepare_environment(config: pytest.Config) -> None:
    """Prepare various environment variables based on the runtime
    configuration.

    :param config: The pytest.Config object.
    """
    if config.option.pw_debug:
        os.environ[EnvironmentVars.PWDEBUG] = "console"
        config.add_cleanup(lambda: os.environ.pop(EnvironmentVars.PWDEBUG))

    if (driver_download_host := config.option.driver_download_host) is not None:
        register_env_defer(
            EnvironmentVars.PLAYWRIGHT_DOWNLOAD_HOST, driver_download_host, config
        )

    if (driver_path := config.option.driver_path) is not None:
        register_env_defer(
            EnvironmentVars.PLAYWRIGHT_BROWSERS_PATH, driver_path, config
        )


@pytest.hookimpl
def pytest_addhooks(pluginmanager: pytest.PytestPluginManager) -> None:
    """Register new `playwright-pytest-enhanced` specific hooking
    functionality."""
    from pytest_playwright_enhanced import hooks as playwright_hooks

    pluginmanager.add_hookspecs(playwright_hooks)


@pytest.hookimpl(trylast=True)
def pytest_playwright_acquire_binaries(config: pytest.Config) -> None:  # noqa: ARG001
    """The default implementation for binary acquisition.

    :param config: The `pytest.Config` object. (auto injected).

    """
    proc_args = ("playwright", "install", "--with-deps")
    completed_process = subprocess.run(
        args=proc_args,
        env=get_driver_env(),
        capture_output=True,
        check=False,
    )
    if completed_process.returncode:
        raise pytest.UsageError("Problem downloading playwright driver binaries!")
    # Todo: implement.
    return pathlib.Path(__file__)


@pytest.hookimpl(trylast=True)
def pytest_playwright_is_debugging(config: pytest.Config) -> bool:  # noqa: ARG001
    """Best effort guess if an IDE etc is debugging the script.  In
    which case launched browser instances will have a forced `headed`
    state.

    :param config: The `pytest.Config` object."""
    return hasattr(sys, "gettrace") and sys.gettrace() is not None


@pytest.hookimpl
def pytest_generate_tests(metafunc: pytest.Metafunc) -> None:
    """Generate iterations of tests based on the browsers specified.
    By default, this plugin will iterate all tests 1:N where N is the
    --browsers provided.  Various markers can impact generation such
    as:

        @pytest.mark.ignore_on_browsers(..., ...)
        @pytest.mark.only_on_browsers(..., ...)

    These markers impact generated tests.
    """
    if not safe_to_run_plugin(metafunc.config):
        return
    node = metafunc.definition.name
    if "pw_multi_browser" in metafunc.fixturenames:
        # tuple is important here to guarantee order in tests.
        allowed_engines = tuple(metafunc.config.option.browser) or ("chromium",)
        for marker in metafunc.definition.iter_markers():
            if marker.name == "pw_only_on_browsers":
                engines = tuple(m.lower() for m in marker.args)
                if any(engine not in allowed_engines for engine in engines):
                    # The user has marked a test with (case insensitive) invalid browser value(s).
                    err_msg = f"Unsupported browser in pw_only_on_browsers in {node}, supported_engines are={allowed_engines}"
                    raise pytest.UsageError(err_msg)
                if not engines:
                    # The user has used an empty @pytest.mark.pw_only_on_browsers() marker
                    err_msg = f"@pytest.mark.pw_only_on_browsers has no values on test: {node}."
                    raise pytest.UsageError(err_msg)
                # We have a valid setup for multi browser based testing.
                allowed_engines = engines
        metafunc.parametrize(argnames="pw_multi_browser", argvalues=allowed_engines)

    # Todo: Consider warning/raising a usage error if using the markers without the multi_browser fixture
    # Tho this is a costly marker iteration process, for now just do checks if fixture is used for multi.


@pytest.fixture(scope=FixtureScope.Function)
def pw_multi_browser() -> None:  # noqa: PT004
    """implicitly parameterizes a test function to run across all three supported
    browsers.  Any test utilising this fixture will be executed 3 times (depending)
    on the markers for only/ignore on certain browsers.

    param pytestconfig: The `pytest.Config` object.

    Returns the currently running browser engine name for the test.

    This is a `meta` fixture and is used/setup properly via the `pytest_generate_tests` hook.
    """


@pytest.fixture(scope=FixtureScope.Function)
def pw_browser_channel(pytestconfig: pytest.Config) -> str | None:
    """Return the browser channel (if specified)."""
    return pytestconfig.option.browser_channel


@pytest.fixture(scope=FixtureScope.Function)
def pw_headed(pytestconfig: pytest.Config) -> bool:
    """Returns `True` if the browser is running headed, else `False` if headless."""
    return pytestconfig.option.headed


@pytest.fixture(scope=FixtureScope.Function)
def pw_device(pytestconfig: pytest.Config) -> bool:
    """Returns the emulated device, if provided."""
    return pytestconfig.option.device


@pytest.fixture(scope=FixtureScope.Function)
def pw_slow_mo(request: pytest.FixtureRequest, pytestconfig: pytest.Config) -> int:
    """Returns the global slow_mofor all actions, defaults to `0`."""
    # We need to inspect the context_kwargs for all overridable things
    # to yield a correct per-test value.
    return parse_browser_kwargs_from_node(request.node, {}).get(
        "slow_mo", pytestconfig.option.slow_mo
    )


@pytest.fixture(scope=FixtureScope.Function)
def pw_playwright() -> typing.Generator[pwsync.Playwright, None, None]:
    """Launch the core playwright context manager, at present only a
    synchronous path is supported however the plan is to add asynchronous
    support in future.
    """
    with pwsync.sync_playwright() as pw:
        yield pw


@pytest.fixture(scope=FixtureScope.Session)
def pw_is_debugging(pytestconfig: pytest.Config) -> bool:
    """Returns if the execution is running with PWDEBUG enabled."""
    return pytestconfig.option.pw_debug


@pytest.fixture(scope=FixtureScope.Function)
def pw_browser_engine(pytestconfig: pytest.Config, pw_multi_browser: None | str) -> str:
    """Return all the browsers provided by the user."""
    # Attempt to get the multi browser call for this particular node.
    # It is not a parameterised test, what is the single browser provided.
    if pw_multi_browser is not None:
        return pw_multi_browser
    options = pytestconfig.option.browser
    if options is None:
        return "chromium"
    if len(options) == 1:
        return options[0]
    # clearly missing test coverage - possibly odd scenarios that can lead to this? - not sure yet.
    raise ValueError(
        "pytest-playwright-enhanced was unable to derive the browser engine - please raise a ticket there."
    )


@pytest.fixture(scope=FixtureScope.Function)
def pw_is_chromium(pw_browser_engine: str) -> bool:
    """Returns true if the running tests will be executed
    on a chromium based browser.

    :param browser_type: The command line flag value for --browser.
    """
    return pw_browser_engine == BrowserEngine.CHROMIUM


@pytest.fixture(scope=FixtureScope.Function)
def pw_is_webkit(pw_browser_engine: str) -> bool:
    """Returns true if the running tests will be executed
    on a webkit based browser.

    :param browser_type: The command line flag value for --browser.
    """
    return pw_browser_engine == BrowserEngine.WEBKIT


@pytest.fixture(scope=FixtureScope.Function)
def pw_is_firefox(pw_browser_engine: str) -> bool:
    """Returns true if the running tests will be executed
    on a firefox based browser.

    :param browser_type: The command line flag value for --browser.
    """
    return pw_browser_engine == BrowserEngine.FIREFOX


@pytest.fixture(scope=FixtureScope.Function)
def pw_root_url(pytestconfig: pytest.Config) -> str:
    """Returns the root url. If provided pages will automatically
    attempt to load this url after creation."""
    return pytestconfig.option.root_url


@pytest.fixture(scope=FixtureScope.Function)
def pw_browser(
    pw_browser_engine: str,
    pw_playwright: pwsync.Playwright,
    pw_browser_kwargs: ContextKwargs,
) -> typing.Generator[pwsync.Browser, None, None]:
    """Yields the core browser instance."""
    try:
        browser = BROWSER_FACTORY[pw_browser_engine](pw_playwright, pw_browser_kwargs)
    except pwsync.Error as err:
        pytest.fail(f"Unable to launch a browser instance because {err!s}")
    else:
        yield browser
        browser.close()


@pytest.fixture(scope=FixtureScope.Function)
def pw_browser_kwargs(
    request: pytest.FixtureRequest, pw_browser_engine: str
) -> ContextKwargs:
    """The configuration to launching browser arguments.  Override this fixture to pass arbitrary
    arguments to the launched Browser instance.

    The complexity in this fixture is 2-fold.  We offer:

        * Global, command line based flags for some defaults
        * User defined capabilities for overriding and applying new launch kwargs via pytest.mark.browser_kwargs

    For the sake of simplicity, the priority is given to pytest.mark options provided for given test, these will
    automatically override any of the defaults that `pytest-playwright-enhanced` offers from the command line.

    Additionally user defined code can completely override this fixture for a bespoke implementation, however
    no merging will then occur and they will be responsible for calculating everything.
    """
    defaults = resolve_commandline_arg_defaults(request.config, pw_browser_engine)

    # Handle some debugging magic, if an IDE or debug mode is detected, automatically
    # force the browsers to open headed.
    is_debugging = request.config.hook.pytest_playwright_is_debugging(
        config=request.config
    )
    if is_debugging:
        defaults["headless"] = False
    return {**defaults, **parse_browser_kwargs_from_node(request.node, {})}


@pytest.fixture(scope=FixtureScope.Function)
def pw_context_kwargs() -> ContextKwargs:
    """The configuration to launching contexts.  Override this fixture to pass arbitrary
    arguments to the launched Context instance.
    """
    return {}


@pytest.fixture(scope=FixtureScope.Function)
def pw_page(
    pytestconfig: pytest.Config,
    pw_context: pwsync.BrowserContext,
) -> typing.Generator[pwsync.Page, None, None]:
    """Launch a new page (tab) as a child of the browser context."""
    page = pw_context.new_page()
    pw_context.pages.append(page)
    if (base_url := pytestconfig.option.root_url) is not None:
        page.goto(base_url)
    yield page
    page.close()


@pytest.fixture(scope=FixtureScope.Function)
def pw_context(
    pw_browser: pwsync.Browser,
    pw_context_kwargs: ContextKwargs,
) -> typing.Generator[pwsync.BrowserContext, None, None]:
    """A scope session scoped browser context."""
    context = pw_browser.new_context(**pw_context_kwargs)
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
