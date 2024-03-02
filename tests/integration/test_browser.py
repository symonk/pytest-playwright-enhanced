import pytest


@pytest.mark.parametrize("browser_type", ["chromium", "webkit", "firefox"])
def test_browser_type_fixture_is_correct(
    pytester: pytest.Pytester,
    browser_type: str,
) -> None:
    pytester.makepyfile(
        f"""
        def test_browser_type(browser_engine):
            assert '{browser_type}' == browser_engine[0]
""",
    )
    result = pytester.runpytest("--browser", browser_type)
    result.assert_outcomes(passed=1)
    assert not result.ret


def test_is_chromium(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_is_chromium(is_chromium, is_webkit, is_firefox):
            assert is_chromium
            assert not is_webkit
            assert not is_firefox
""",
    )
    result = pytester.runpytest(["--browser", "chromium"])
    result.assert_outcomes(passed=1)


def test_is_webkit(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_is_webkit(is_chromium, is_webkit, is_firefox):
            assert not is_chromium
            assert is_webkit
            assert not is_firefox
""",
    )
    result = pytester.runpytest("--browser", "webkit")
    result.assert_outcomes(passed=1)


def test_is_firefox(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_is_firefox(is_chromium, is_webkit, is_firefox):
            assert not is_chromium
            assert not is_webkit
            assert is_firefox
""",
    )
    result = pytester.runpytest("--browser", "firefox")
    result.assert_outcomes(passed=1)


def test_unsupported_browser(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--browser", "no")
    result.stderr.fnmatch_lines(
        "*error: argument --browser: invalid choice: 'no' (choose from 'chromium', 'webkit', 'firefox')",
    )
    assert result.ret == pytest.ExitCode.USAGE_ERROR
