from enum import Enum


class FixtureScopes(str, Enum):
    Function = "function"
    Session = "session"
