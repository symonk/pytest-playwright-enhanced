from dataclasses import dataclass


@dataclass(frozen=True)
class FixtureScope:
    Function: str = "function"
    Session: str = "session"


@dataclass(frozen=True)
class BrowserEngine:
    CHROMIUM: str = "chromium"
    WEBKIT: str = "webkit"
    FIREFOX: str = "firefox"


@dataclass(frozen=True)
class EnvironmentVars:
    PWDEBUG = "PWDEBUG"
    PLAYWRIGHT_DOWNLOAD_HOST = "PLAYWRIGHT_DOWNLOAD_HOST"
    PLAYWRIGHT_BROWSERS_PATH = "PLAYWRIGHT_BROWSERS_PATH"
    PYTEST_CURRENT_TEST = "PYTEST_CURRENT_TEST"


# This is a tuple, not set as order is important.
SupportedBrowsers = (
    BrowserEngine.CHROMIUM,
    BrowserEngine.FIREFOX,
    BrowserEngine.WEBKIT,
)
