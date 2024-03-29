import pytest

from ..utils import artifact_files

pytestmark = pytest.mark.artifacts


def test_can_override_page_screenshot_timeout(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_timeout_override(pytestconfig):
        assert pytestconfig.option.screenshot_timeout == '5000'
""")
    pytester.runpytest("--screenshot-timeout", 5000).assert_outcomes(passed=1)


def test_video_action_without_supported(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--video-on-fail", "unsupported")
    result.stderr.fnmatch_lines(
        ["*can only be 'yes', 'no' or a width x height string such as '800x640'*"]
    )
    assert result.ret == pytest.ExitCode.USAGE_ERROR


def test_video_action_without_width_integer(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--video-on-fail", "nox800")
    result.stderr.fnmatch_lines(["*width x height option must both be valid integers*"])
    assert result.ret == pytest.ExitCode.USAGE_ERROR


def test_video_action_without_height_integer(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--video-on-fail", "1024xno")
    result.stderr.fnmatch_lines(["*width x height option must both be valid integers*"])
    assert result.ret == pytest.ExitCode.USAGE_ERROR


def test_artifacts_directory_exists(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_artifacts_dir_is_created(pw_artifacts_dir):
            assert pw_artifacts_dir.is_dir()
            assert not any(pw_artifacts_dir.iterdir())
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_video_on_fail_enabled(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.video_on_fail == "yes"
""")
    pytester.runpytest("--video-on-fail", "yes").assert_outcomes(passed=1)


def test_video_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.video_on_fail == "no"
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_screenshot_on_fail_enabled(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.screenshots_on_fail == "yes"
""")
    pytester.runpytest("--screenshots-on-fail", "yes").assert_outcomes(passed=1)


def test_screenshot_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.screenshots_on_fail == "no"
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_trace_on_fail_enabled(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.trace_on_fail
""")
    pytester.runpytest("--trace-on-fail").assert_outcomes(passed=1)


def test_trace_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert not pytestconfig.option.trace_on_fail
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_videos_are_stored_in_artifacts_folder(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_fails_with_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(launch_browser_flags, "--video-on-fail", "yes")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    expected = {"test-fails-with-video-chromium-0.webm"}
    assert expected == artifact_files(pytester, "webm")


def test_videos_are_stored_when_width_height_is_specified(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_fails_with_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(launch_browser_flags, "--video-on-fail", "1024x768")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert {"test-fails-with-video-chromium-0.webm"} == artifact_files(pytester, "webm")


def test_videos_are_not_stored_in_artifacts_folder(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_fails_without_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(launch_browser_flags)
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert not artifact_files(pytester, "webm")


def test_multiple_pages_returns_multiple_videos_in_artifacts(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_multiple_pages(pw_context):
            one = pw_context.new_page()
            two = pw_context.new_page()
            one.goto("https://www.google.com")
            two.goto("https://www.google.com")
            # Fail to retain videos
            assert False
""")
    result = pytester.runpytest(launch_browser_flags, "--video-on-fail", "yes")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    expected_files = {
        "test-multiple-pages-chromium-0.webm",
        "test-multiple-pages-chromium-1.webm",
    }
    assert artifact_files(pytester, "webm") == expected_files


def test_multiple_pages_returns_multiple_videos_when_width_height_is_set(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile("""
        def test_multiple_pages(pw_context):
            one = pw_context.new_page()
            two = pw_context.new_page()
            one.goto("https://www.google.com")
            two.goto("https://www.google.com")
            # Fail to retain videos
            assert False
""")
    result = pytester.runpytest(launch_browser_flags, "--video-on-fail", "1024x768")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    expected_files = {
        "test-multiple-pages-chromium-0.webm",
        "test-multiple-pages-chromium-1.webm",
    }
    assert artifact_files(pytester, "webm") == expected_files


def test_videos_are_removed_when_passing_regardless(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_success_no_videos(pw_page):
            pw_page.goto("https://www.google.com")
            assert True
""")
    pytester.runpytest(launch_browser_flags, "--video-on-fail", "yes")
    assert not artifact_files(pytester, "webm")


def test_multiple_videos_with_xdist_is_correct(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
    def test_xdist(pw_page, pw_multi_browser):
        pw_page.goto("https://www.google.com")
        assert False
""")
    pytester.runpytest(
        launch_browser_flags,
        "-n",
        3,
        "--browser",
        "webkit",
        "--browser",
        "firefox",
        "--browser",
        "chromium",
        "--video-on-fail",
        "yes",
    ).assert_outcomes(failed=3)
    assert {
        "test-xdist-chromium-0.webm",
        "test-xdist-webkit-0.webm",
        "test-xdist-firefox-0.webm",
    } == artifact_files(pytester, "webm")


def test_tracing_enabled_writes_an_artifact_successfully(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_tracing_artifacts_are_kept(pw_page):
            assert False
""")
    result = pytester.runpytest(launch_browser_flags, "--trace-on-fail")
    result.assert_outcomes(failed=1)
    files = artifact_files(pytester, "zip")
    assert {"test-tracing-artifacts-are-kept-chromium-trace.zip"} == files


def test_tracing_deletes_artifact_when_test_passes_and_enabled(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_tracing_artifacts_are_removed(pw_page):
            assert True
""")
    result = pytester.runpytest(launch_browser_flags, "--trace-on-fail")
    result.assert_outcomes(passed=1)
    assert set() == artifact_files(pytester, "zip")


def test_tracing_has_no_artifacts_when_disabled(
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_tracing_artifacts_are_removed(pw_page):
            assert True
""")
    result = pytester.runpytest(launch_browser_flags)
    result.assert_outcomes(passed=1)
    assert set() == artifact_files(pytester, "zip")


@pytest.mark.parametrize("mode", ["yes", "full"])
def test_multiple_pages_store_multiple_screenshots(
    mode: str,
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_multiple_pages_store_multiple_screenshots(pw_context):
            for _ in range(3):
                p = pw_context.new_page()
                p.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(launch_browser_flags, "--screenshots-on-fail", mode)
    result.assert_outcomes(failed=1)
    screenshots = {
        "test-multiple-pages-store-multiple-screenshots-chromium-0.png",
        "test-multiple-pages-store-multiple-screenshots-chromium-1.png",
        "test-multiple-pages-store-multiple-screenshots-chromium-2.png",
    }
    assert screenshots == artifact_files(pytester, "png")


@pytest.mark.parametrize("mode", ["yes", "full"])
def test_when_passing_with_screenshot_flag_no_screenshots(
    mode: str,
    pytester: pytest.Pytester,
    launch_browser_flags: str,
) -> None:
    pytester.makepyfile("""
        def test_no_screenshots_on_pass():
            assert True
""")
    result = pytester.runpytest(launch_browser_flags, "--screenshots-on-fail", mode)
    result.assert_outcomes(passed=1)
    assert set() == artifact_files(pytester, "png")


def test_when_failing_without_flag_no_screenshots(
    pytester: pytest.Pytester, launch_browser_flags: str
) -> None:
    pytester.makepyfile("""
        def test_no_screenshots_on_fail_default():
            assert False
""")
    result = pytester.runpytest(launch_browser_flags)
    result.assert_outcomes(failed=1)
    assert set() == artifact_files(pytester, "png")


# Todo: Add a test that encompasses all 3 artifacts, for multiple spawned pages in each
