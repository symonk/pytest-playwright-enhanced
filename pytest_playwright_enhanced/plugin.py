import pytest
from playwright import sync_api as pwsync


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
        action="store",
        # Todo: implement choice(s).
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


@pytest.fixture
def page() -> pwsync.Page:
    """A fresh page instance between tests."""
    ...


@pytest.fixture(scope="session")
def context() -> pwsync.BrowserContext:
    """A scope session scoped browser context."""
