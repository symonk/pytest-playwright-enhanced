import pytest

pytestmark = pytest.mark.output


def test_plugin_is_registered(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest()
    result.stdout.fnmatch_lines(["*plugins:*playwright-enhanced-0.2.0*"])


def test_help_is_correct(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--help")
    result.stdout.fnmatch_lines(
        [
            "*Batteries included playwright for pytest:",
            "*--headed*Should tests be ran headed. (Defaults to headless)*",
            "*--base-url*The base_url that is loaded by pages. (Defaults to*",
        ]
    )
    assert result.ret == pytest.ExitCode.OK


def test_fixtures_is_correct(pytester: pytest.Pytester) -> None:
    result = pytester.runpytest("--fixtures")
    result.stdout.fnmatch_lines([])
    assert result.ret == pytest.ExitCode.OK
