import pytest


def test_running_multiple_browsers_parameterized(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_basic_browsers(request, pw_multi_browser):
        if "chromium" in request.node.name:
            assert pw_multi_browser == "chromium"
        if "webkit" in request.node.name:
            assert pw_multi_browser == "webkit"
        if "firefox" in request.node.name:
            assert pw_multi_browser == "firefox"
""")
    result = pytester.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    )
    result.assert_outcomes(passed=3)
    assert result.ret == pytest.ExitCode.OK


@pytest.mark.parametrize("only_engine", ["chromium", "firefox", "webkit"])
def test_only_on_browsers_works_correctly(
    pytester: pytest.Pytester, only_engine: str
) -> None:
    pytester.makepyfile(f"""
        import pytest

        @pytest.mark.pw_only_on_browsers("{only_engine}")
        def test_only_on_browser_marker(pw_multi_browser):
            assert pw_multi_browser == "{only_engine}"
""")
    pytester.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    ).assert_outcomes(passed=1)


def test_unsupported_browser_in_only_runs_on(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest
        @pytest.mark.pw_only_on_browsers("chromium", "foo")
        def test_unsupported_only_on_browsers(pw_multi_browser):
            ...
""")
    result = pytester.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    )
    result.assert_outcomes(errors=1)
    assert result.ret == pytest.ExitCode.INTERRUPTED
    err = "*UsageError: Unsupported browser in pw_only_on_browsers in test_unsupported_only_on_browsers, supported_engines are=('chromium', 'firefox', 'webkit')*"
    result.stdout.fnmatch_lines([err])


def test_removing_all_browsers_raises_usage_error(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest
        @pytest.mark.pw_only_on_browsers()
        def test_no_browsers_with_only_on(pw_multi_browser):
            ...
""")
    result = pytester.runpytest(
        "--browser", "chromium", "--browser", "firefox", "--browser", "webkit"
    )
    result.assert_outcomes(errors=1)
    assert result.ret == pytest.ExitCode.INTERRUPTED
    err = "*UsageError: @pytest.mark.pw_only_on_browsers has no values on test: test_no_browsers_with_only_on."
    result.stdout.fnmatch_lines([err])


@pytest.mark.parametrize("engine", ["chromium", "firefox", "webkit"])
def test_browser_engine_fixture_is_accurate(
    pytester: pytest.Pytester, engine: str
) -> None:
    pytester.makepyfile(f"""
        import pytest

        def test_accurate_browser_engine(pw_multi_browser, pw_browser_engine):
            assert pw_multi_browser == "{engine}"
            assert pw_browser_engine == "{engine}"
""")
    result = pytester.runpytest("--browser", engine)
    result.assert_outcomes(passed=1)
