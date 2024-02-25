import pytest


def test_plugin_is_registered(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest()
    result.stdout.fnmatch_lines(["*plugins: playwright-enhanced-0.1.0*"])


def test_help_is_correct(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--help")
    result.stdout.fnmatch_lines([])
    assert result.ret == pytest.ExitCode.OK


def test_fixtures_is_correct(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--fixtures")
    result.stdout.fnmatch_lines([])
    assert result.ret == pytest.ExitCode.OK
