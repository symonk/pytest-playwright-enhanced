from enum import Enum


class FixtureScopes(str, Enum):
    Function = "function"
    Session = "session"


class BrowserName(str, Enum):
    CHROMIUM = "chromium"
    WEBKIT = "webkit"
    FIREFOX = "firefox"
