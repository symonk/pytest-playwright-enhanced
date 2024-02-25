import pytest


def test_sync_playwright_is_available(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        from playwright.sync_api import Playwright

        def test_sync_playwright(playwright):
            assert isinstance(playwright, Playwright)
""",
    )
    result = pytester.runpytest()
    assert result.ret == 0
