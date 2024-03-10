pytest_plugins = ["pytester"]
import pathlib
import sys

import pytest


@pytest.fixture(scope="session")
def drivers_path() -> str:
    """Used to allow tox runs to use the ~/.cache/ms-playwright/ binaries
    for the actual user.  This is **NOT** overly clean, there must be a
    better tox method for handling this, we do not want to have to download
    browser binaries on every run - they are expensive and sizabl!"""
    if sys.platform == "linux":
        return str(pathlib.Path.expanduser(pathlib.Path("~/.cache/ms-playwright/")))
    if sys.platform == "win32":
        return str(
            pathlib.Path.expanduser(pathlib.Path("~/AppData/Local/ms-playwright/"))
        )
    if sys.platform == "darwin":
        return str(
            pathlib.path.expanduser(pathlib.path("~/Libary/Caches/ms-playwright/"))
        )
    raise ValueError("undetected operating system for using reusable binaries.")
