import pytest


def test_root_url_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_root_url(root_url):
            assert root_url is None
    """,
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_root_url_override(pytester: pytest.Pytester) -> None:
    url = "https://www.google.com"
    pytester.makepyfile(
        f"""
        def test_root_url(root_url):
            assert root_url == '{url}'
    """,
    )
    result = pytester.runpytest("--root-url", url)
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK
