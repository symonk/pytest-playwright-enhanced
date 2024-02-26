import pytest


def test_headless_is_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
            def test_headed(headed):
                assert not headed
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_headed_can_be_overriden(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_headless(headed):
            assert headed
    """
    )
    result = pytester.runpytest("--headed")
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK
