pytest_plugins = ["pytester"]
import os
import pathlib

import pytest


# Allow us to use downloaded binaries for now; this is only setup for linux
# based development.  See: https://playwright.dev/docs/browsers for adding
# support to windows/mac OSX based support.  Eventually PWE will be able
# to properly auto acquire binaries on the users behalf and this will go
# away.
@pytest.mark.hookimpl(trylast=True)
def pytest_configure() -> None:
    os.environ.setdefault(
        "PLAYWRIGHT_BROWSERS_PATH",
        str(pathlib.Path.home() / ".cache" / "ms-playwright"),
    )


@pytest.fixture(scope="session")
def drivers_path() -> str:
    """Used to allow tox runs to use the ~/.cache/ms-playwright/ binaries
    for the actual user.  This is **NOT** overly clean, there must be a
    better tox method for handling this, we do not want to have to download
    browser binaries on every run - they are expensive and sizabl!"""
    return str(pathlib.Path(f"{os.environ['HOME']}") / ".cache" / "ms-playwright") + "/"
