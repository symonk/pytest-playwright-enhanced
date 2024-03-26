from __future__ import annotations

from playwright.sync_api import Page


class PlaywrightEnhancedPage:
    """An improved Page object."""

    def __init__(self: PlaywrightEnhancedPage, page: Page) -> None:
        self.page = page
