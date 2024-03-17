import pytest

pytestmark = pytest.mark.artifacts


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
        assert pytestconfig.option.video_on_fail
""")
    pytester.runpytest("--video-on-fail").assert_outcomes(passed=1)


def test_video_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert not pytestconfig.option.video_on_fail
""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_screenshot_on_fail_enabled(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.screenshots == "yes"
""")
    pytester.runpytest("--screenshots", "yes").assert_outcomes(passed=1)


def test_screenshot_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.screenshots == "no"
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
            assert False

        def test_video_was_written(pw_artifacts_dir):
            files = []
            for f in pw_artifacts_dir.iterdir():
                if f.is_file():
                    files.append(f)
            assert len(files) == 1
            assert files[0].name.endswith(".webm")
""")
    result = pytester.runpytest(drivers_path, "--video-on-fail")
    result.assert_outcomes(passed=1, failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_videos_are_not_stored_in_artifacts_folder(
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
        def test_fails_without_video(pw_page):
            assert False

        def test_video_was_not_written(pw_artifacts_dir):
            assert not any(pw_artifacts_dir.iterdir())
""")
    result = pytester.runpytest(drivers_path)
    result.assert_outcomes(passed=1, failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_screenshots_are_stored_in_artifacts_folder() -> None: ...
def test_screenshots_are_not_stored_in_artifacts_folder() -> None: ...


def test_traces_are_stored_in_artifacts_folder() -> None: ...
def test_traces_are_not_stored_in_artifacts_folder() -> None: ...
