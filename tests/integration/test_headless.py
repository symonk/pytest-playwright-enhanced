import pytest


def test_headless_is_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
            def test_headed(headed):
                assert not headed
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_headed_can_be_overriden(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_headless(headed):
            assert headed
    """
    )
    result = pytester.runpytest("--headed")
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


@pytest.mark.skip(reason="not implemented!")
def test_browser_is_launched_headlessly(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_browser_is_actually_headless(page, headed):
            assert headed
            page.goto("https://www.google.com")
"""
    )
    result = pytester.runpytest("--headed")
    result.assert_outcomes(passed=1)
