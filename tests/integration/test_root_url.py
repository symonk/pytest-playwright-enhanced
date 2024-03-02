import pytest


def test_root_url_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_root_url(pw_root_url):
            assert pw_root_url is None
    """,
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_root_url_override(pytester: pytest.Pytester) -> None:
    url = "https://www.google.com"
    pytester.makepyfile(
        f"""
        def test_root_url(pw_root_url):
            assert pw_root_url == '{url}'
    """,
    )
    result = pytester.runpytest("--root-url", url)
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_root_url_can_be_override_in_user_space(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        @pytest.fixture(scope="session")
        def pw_root_url():
            return "https://www.google.com"

        def test_override_root_url(pw_root_url):
            assert pw_root_url == "https://www.google.com"

    """,
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
