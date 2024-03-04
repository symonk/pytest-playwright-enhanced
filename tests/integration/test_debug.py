import pytest

pytestmark = pytest.mark.debug


def test_debug_env_is_set_when_requested(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import os
        def test_env_set():
            assert os.environ["PWDEBUG"] == "console"

        def test_is_debugging_yes(pw_is_debugging):
            assert pw_is_debugging
""",
    )
    result = pytester.runpytest("--pw-debug")
    result.assert_outcomes(passed=2)


def test_debug_env_is_not_set_by_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import os
        def test_env_not_set():
            assert "PWDEBUG" not in os.environ

        def test_not_is_debugging(pw_is_debugging):
            assert not pw_is_debugging
""",
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=2)
