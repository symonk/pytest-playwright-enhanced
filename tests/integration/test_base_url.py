import pytest

pytestmark = pytest.mark.base_url


def test_base_url_default(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        def test_base_url(pw_base_url):
            assert pw_base_url is None
    """,
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_base_url_override(pytester: pytest.Pytester) -> None:
    url = "https://www.google.com"
    pytester.makepyfile(
        f"""
        def test_base_url(pw_base_url):
            assert pw_base_url == '{url}'
    """,
    )
    result = pytester.runpytest("--base-url", url)
    result.assert_outcomes(passed=1)
    assert result.ret == pytest.ExitCode.OK


def test_base_url_can_be_override_in_user_space(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        @pytest.fixture
        def pw_base_url():
            return "https://www.google.com"

        def test_override_base_url(pw_base_url):
            assert pw_base_url == "https://www.google.com"

    """,
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)
