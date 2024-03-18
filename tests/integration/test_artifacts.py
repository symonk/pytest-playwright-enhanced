import pytest

from ..utils import artifact_files

pytestmark = pytest.mark.artifacts


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
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
        def test_fails_with_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(drivers_path, "--video-on-fail", "yes")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    expected = {"test-fails-with-video-chromium-0.webm"}
    assert expected == artifact_files(pytester, "webm")


def test_videos_are_stored_when_width_height_is_specified(
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
        def test_fails_with_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(drivers_path, "--video-on-fail", "1024x768")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert {"test-fails-with-video-chromium-0.webm"} == artifact_files(pytester, "webm")


def test_videos_are_not_stored_in_artifacts_folder(
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
        def test_fails_without_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False
""")
    result = pytester.runpytest(drivers_path)
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    assert not artifact_files(pytester, "webm")


def test_multiple_pages_returns_multiple_videos_in_artifacts(
    pytester: pytest.Pytester, drivers_path: str
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
    result = pytester.runpytest(drivers_path, "--video-on-fail", "yes")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    expected_files = {
        "test-multiple-pages-chromium-0.webm",
        "test-multiple-pages-chromium-1.webm",
    }
    assert artifact_files(pytester, "webm") == expected_files


def test_multiple_pages_returns_multiple_videos_when_width_height_is_set(
    pytester: pytest.Pytester, drivers_path: str
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
    result = pytester.runpytest(drivers_path, "--video-on-fail", "1024x768")
    result.assert_outcomes(failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED
    expected_files = {
        "test-multiple-pages-chromium-0.webm",
        "test-multiple-pages-chromium-1.webm",
    }
    assert artifact_files(pytester, "webm") == expected_files


def test_videos_are_removed_when_passing_regardless(
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
        def test_success_no_videos(pw_page):
            pw_page.goto("https://www.google.com")
            assert True
""")
    pytester.runpytest(drivers_path, "--video-on-fail", "yes")
    assert not artifact_files(pytester, "webm")


def test_screenshots_are_stored_in_artifacts_folder() -> None: ...
def test_screenshots_are_not_stored_in_artifacts_folder() -> None: ...


def test_traces_are_stored_in_artifacts_folder() -> None: ...
def test_traces_are_not_stored_in_artifacts_folder() -> None: ...


def test_multiple_videos_with_xdist_is_correct(
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
    def test_xdist(pw_page, pw_multi_browser):
        pw_page.goto("https://www.google.com")
        assert False
""")
    pytester.runpytest(
        drivers_path,
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
