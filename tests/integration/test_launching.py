import pytest


@pytest.mark.skip(reason="not implemented.")
def test_can_launch_browser(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_launch_browser(page):
            page.goto("https://www.google.com")
""",
    )
    result = pytester.runpytest()
    assert result.assert_outcomes(passed=1)
