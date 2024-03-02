pytest_plugins = ["pytester"]
import os
import pathlib

# Allow us to use downloaded binaries for now; this is only setup for linux
# based development.  See: https://playwright.dev/docs/browsers for adding
# support to windows/mac OSX based support.  Eventually PWE will be able
# to properly auto acquire binaries on the users behalf and this will go
# away.
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(
    pathlib.Path.home() / ".cache" / "ms-playwright"
)
