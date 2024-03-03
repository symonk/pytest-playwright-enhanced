import pytest


def test_sync_playwright_is_available(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        from playwright.sync_api import Playwright

        def test_sync_playwright(pw_playwright):
            assert isinstance(pw_playwright, Playwright)
""",
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert not result.ret
