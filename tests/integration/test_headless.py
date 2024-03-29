import pytest

pytestmark = pytest.mark.headless


def test_headless_is_default(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile(
        """
            def test_headed(pw_page, pw_headed):
                assert not pw_headed
                user_agent = pw_page.evaluate("window.navigator.userAgent;")
                assert "HeadlessChrome" in user_agent
    """
    )
    result = pytester.runpytest(launch_browser_flags, "-s")
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_browser_is_launched_headlessly(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile(
        """
        def test_browser_is_actually_headless(pw_page, pw_headed):
            assert pw_headed
            user_agent = pw_page.evaluate("navigator.userAgent;")
            assert "HeadlessChrome" not in user_agent
            assert "Chrome" in user_agent
"""
    )
    result = pytester.runpytest("--headed", launch_browser_flags)
    result.assert_outcomes(passed=1)
