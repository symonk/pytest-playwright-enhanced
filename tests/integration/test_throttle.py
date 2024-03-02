import pytest


def test_global_throttle_is_applied(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_throttle_global(pw_throttle):
            assert pw_throttle == 10.25
""")
    result = pytester.runpytest("--throttle", "10.25")
    result.assert_outcomes(passed=1)


def test_default_throttle_is_zero(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_throttle_global(pw_throttle):
            assert pw_throttle == 0.0
""")
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


@pytest.mark.skip("not implemented yet!")
def test_per_test_throttle(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest
        import time

        @pytest.mark.context_kwargs({'throttle': 1000})
        def test_throttle_override_per_test(page, pw_throttle):
            now = int(time.now())
            page.goto('https://www.google.com')
            since = int(time.time()) - now
            assert since > pw_throttle
""")
    result = pytester.runpytest("--throttle", "3000")
    result.assert_outcomes(passed=1)
