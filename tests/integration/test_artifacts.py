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
        assert pytestconfig.option.screenshot_on_fail
""")
    pytester.runpytest("--screenshot-on-fail").assert_outcomes(passed=1)


def test_screenshot_on_fail_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
    def test_default(pytestconfig):
        assert not pytestconfig.option.screenshot_on_fail
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
