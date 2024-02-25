from enum import Enum


class FixtureScope(str, Enum):
    Function = "function"
    Session = "session"


class BrowserEngine(str, Enum):
    CHROMIUM = "chromium"
    WEBKIT = "webkit"
    FIREFOX = "firefox"
