from pytest_playwright_enhanced.const import BrowserEngine
from pytest_playwright_enhanced.const import FixtureScope


def test_browser_engines_dataclass() -> None:
    assert BrowserEngine.CHROMIUM == "chromium"
    assert BrowserEngine.FIREFOX == "firefox"
    assert BrowserEngine.WEBKIT == "webkit"


def test_fixture_scopes_dataclass() -> None:
    assert FixtureScope.Function == "function"
    assert FixtureScope.Session == "session"
