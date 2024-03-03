import pytest


def test_global_slow_mo_is_applied(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_slow_mo_global(pw_slow_mo):
            assert pw_slow_mo == 10
""")
    result = pytester.runpytest("--slow-mo", "10")
    result.assert_outcomes(passed=1)


def test_default_slow_mo_is_zero(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_slow_mo_global(pw_slow_mo):
            assert pw_slow_mo == 0
""")
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


@pytest.mark.skip()
def test_slow_mo_can_be_set_on_a_test_level(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest
        import time

        @pytest.mark.browser_kwargs(config={'slow_mo': 1000})
        def test_slow_mo_override_per_test(pw_page, pw_slow_mo):
            assert pw_slow_mo == 1000
""")
    result = pytester.runpytest("--slow-mo", "3000")
    result.assert_outcomes(passed=1)
