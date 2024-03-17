import pytest

pytestmark = pytest.mark.artifacts


def test_video_action_without_supported(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--videos-on-fail", "unsupported")
    result.stderr.fnmatch_lines(
        ["*can only be 'yes', 'no' or a width x height string such as '800x640'*"]
    )
    assert result.ret == pytest.ExitCode.USAGE_ERROR


def test_video_action_without_width_integer(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--videos-on-fail", "nox800")
    result.stderr.fnmatch_lines(["*width x height option must both be valid integers*"])
    assert result.ret == pytest.ExitCode.USAGE_ERROR


def test_video_action_without_height_integer(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--videos-on-fail", "1024xno")
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
        assert pytestconfig.option.videos_on_fail == "yes"
""")
    pytester.runpytest("--videos-on-fail", "yes").assert_outcomes(passed=1)


def test_video_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert pytestconfig.option.videos_on_fail == "no"
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

        def test_video_was_written(pw_artifacts_dir):
            files = []
            for f in pw_artifacts_dir.iterdir():
                if f.is_file():
                    files.append(f)
            assert len(files) == 1
            assert files[0].name.endswith(".webm")
""")
    result = pytester.runpytest(drivers_path, "--videos-on-fail", "yes")
    result.assert_outcomes(passed=1, failed=1)
    assert result.ret == pytest.ExitCode.TESTS_FAILED


def test_videos_are_stored_when_width_height_is_specified(
    pytester: pytest.Pytester, drivers_path: str
) -> None:
    pytester.makepyfile("""
        def test_fails_with_video(pw_page):
            pw_page.goto("https://www.google.com")
            assert False

        def test_video_was_written_with_width_height(pw_artifacts_dir):
            files = []
            for f in pw_artifacts_dir.iterdir():
                if f.is_file():
                    files.append(f)
            assert len(files) == 1
            assert files[0].name.endswith(".webm")
""")
    result = pytester.runpytest(drivers_path, "--videos-on-fail", "1024x768")
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


# Todo Videos, screenshots & traces for their bespoke 3rd options.
