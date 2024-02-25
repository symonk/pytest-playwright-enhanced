from dataclasses import dataclass


@dataclass
class FixtureScope:
    Function: str = "function"
    Session: str = "session"


class BrowserEngine:
    CHROMIUM: str = "chromium"
    WEBKIT: str = "webkit"
    FIREFOX: str = "firefox"
