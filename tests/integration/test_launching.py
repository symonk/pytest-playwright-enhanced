import pytest

pytestmark = pytest.mark.launching


@pytest.mark.skip(reason="not implemented.")
def test_can_launch_browser(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_launch_browser(page):
            page.goto("https://www.google.com")
""",
    )
    result = pytester.runpytest("--acquire-drivers", "--headed")
    result.assert_outcomes(passed=1)


def test_acquire_drivers_on(pytester: pytest.Pytester) -> None:
    _ = pytester


def test_acquire_drivers_off(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_acquisition_off(pytestconfig):
            assert pytestconfig.option.acquire_drivers == "no"
"""
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_acquire_drivers_with_deps(pytester: pytest.Pytester) -> None:
    _ = pytester
