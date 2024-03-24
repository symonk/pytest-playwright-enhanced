import pytest

pytestmark = pytest.mark.browsers


# This test will break for webkit if you have a snap install of Vscode.
# https://github.com/microsoft/playwright/issues/23899
# I tried modifying the settings.json in .vscode/ but to no avail
# I reinstalled vscode w/o snap to resolve.
def test_can_launch_browsers_of_types(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile("""

    def test_runs_all_browsers(pw_page, pw_multi_browser):
        pw_page.goto("https://www.google.com")
""")
    pytester.runpytest(
        "--pw-debug",
        "--browser",
        "chromium",
        "--browser",
        "firefox",
        "--browser",
        "webkit",
        launch_browser_flags,
    ).assert_outcomes(passed=3)


@pytest.mark.parametrize("browser_type", ["chromium", "webkit", "firefox"])
def test_browser_type_fixture_is_correct(
    pytester: pytest.Pytester,
    browser_type: str,
) -> None:
    pytester.makepyfile(
        f"""
        def test_browser_type(pw_browser_engine):
            assert '{browser_type}' == pw_browser_engine
""",
    )
    result = pytester.runpytest("--browser", browser_type)
    result.assert_outcomes(passed=1)
    assert not result.ret


def test_is_chromium(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_is_chromium_foo(pw_is_chromium, pw_is_webkit, pw_is_firefox):
            assert pw_is_chromium
            assert not pw_is_webkit
            assert not pw_is_firefox
""",
    )
    result = pytester.runpytest("--browser", "chromium")
    result.assert_outcomes(passed=1)


def test_is_webkit(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_is_webkit(pw_is_chromium, pw_is_webkit, pw_is_firefox):
            assert not pw_is_chromium
            assert pw_is_webkit
            assert not pw_is_firefox
""",
    )
    result = pytester.runpytest("--browser", "webkit")
    result.assert_outcomes(passed=1)


def test_is_firefox(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_is_firefox(pw_is_chromium, pw_is_webkit, pw_is_firefox):
            assert not pw_is_chromium
            assert not pw_is_webkit
            assert pw_is_firefox
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


def test_all_browser_overrides_fixture(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile("""
    import pytest

    @pytest.mark.browser_kwargs(
        channel="chrome",
        slow_mo=10.00,
        timeout=45_000,
        chromium_sandbox=True,
    )
    def test_browser_kwargs_from_marker(pw_browser_kwargs):
        assert pw_browser_kwargs['channel'] == "chrome"
        assert pw_browser_kwargs['slow_mo'] == 10.00
        assert pw_browser_kwargs['timeout'] == 45_000
        assert pw_browser_kwargs['chromium_sandbox']

""")
    pytester.runpytest(launch_browser_flags).assert_outcomes(passed=1)


def test_all_browser_overrides_marker(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile("""

    import pytest

    @pytest.fixture()
    def pw_browser_kwargs():
        return {
            "slow_mo": 5.00,
            "timeout": 30_000,
            "chromium_sandbox": True,

        }

    def test_overriden_kwargs_browser(pw_browser):
        assert pw_browser.is_connected()
    """)
    pytester.runpytest(launch_browser_flags).assert_outcomes(passed=1)


def test_browser_kwargs_defaults(pytester: pytest.Pytester) -> None:
    exe_path = "/tmp/foo"
    channel = "chrome-dev"
    timeout = 50_000
    pytester.makepyfile(f"""
    def test_browser_kwargs_default(pw_browser_kwargs):
        assert pw_browser_kwargs['executable_path'] == '{exe_path}'
        assert pw_browser_kwargs['channel'] == '{channel}'
        assert pw_browser_kwargs['timeout'] == {timeout}
        assert pw_browser_kwargs['chromium_sandbox']
        assert not pw_browser_kwargs['headless']
        assert pw_browser_kwargs['handle_sighup']
        assert pw_browser_kwargs['handle_sigint']
        assert pw_browser_kwargs['handle_sigterm']
""")
    pytester.runpytest(
        "--headed",
        "--executable-path",
        exe_path,
        "--channel",
        channel,
        "--browser-timeout",
        timeout,
        "--chromium-sandbox",
    ).assert_outcomes(passed=1)


def test_browser_kwargs_with_user_defined_overrides(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_stub():
        ...
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_browser_kwargs_with_args_raises_pwe_error(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest
        @pytest.mark.browser_kwargs(100, 200)
        def test_will_fail_with_raises_browser_kwargs(pw_browser_kwargs):
            ...
""")
    result = pytester.runpytest()
    result.assert_outcomes(errors=1)
    expected = "*pytest_playwright_enhanced.exceptions.PWEMarkerError: `@pytest.mark.browser_kwargs` only supports keyword args. Test(test_will_fail_with_raises_browser_kwargs*) used args=(100, 200)"
    result.stdout.fnmatch_lines([expected])
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_dynamic_callback_is_merged(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest

        def cb(item):
            return {"item": item.name}

        @pytest.mark.browser_kwargs(item="overridden", callback=cb)
        def test_merged_dynamic_callback(request, pw_browser_kwargs):
            assert pw_browser_kwargs['item'] == request.node.name
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_default_browser_kwargs_has_no_proxy(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_default_proxy(pw_browser_kwargs):
            assert pw_browser_kwargs.get("proxy") is None
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_custom_plugin_overwrites_proxy(pytester: pytest.Pytester) -> None:
    pytester.makeconftest("""
        import pytest
        from playwright.sync_api import ProxySettings

        @pytest.hookimpl
        def pytest_playwright_configure_proxy(config):
            return ProxySettings(server="foo", bypass="bar", username="baz", password="no")
""")
    pytester.makepyfile("""
        def test_overwritten_proxy(pw_browser_kwargs):
            assert pw_browser_kwargs['server'] == 'foo'
            assert pw_browser_kwargs['bypass'] == 'bar'
            assert pw_browser_kwargs['username'] == 'baz'
            assert pw_browser_kwargs['password'] == 'no'
""")
    pytester.runpytest().assert_outcomes(passed=True)
