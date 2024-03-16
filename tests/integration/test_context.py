import pytest

pytestmark = pytest.mark.context


def test_context_kwargs_fixture_override(pytester: pytest.Pytester) -> None:
    pytester.makepyfile(
        """
        import pytest

        @pytest.fixture(scope='function')
        def pw_context_args():
            return {'foo': 'bar'}

        def test_context_kwargs(pw_context_args):
            assert pw_context_args == {'foo': 'bar'}
    """
    )
    result = pytester.runpytest()
    result.assert_outcomes(passed=1)


def test_context_kwargs_defaults(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        def test_context_kwargs_defaults(pw_context_kwargs):
            expected = {}
            assert pw_context_kwargs == expected

""")
    pytester.runpytest().assert_outcomes(passed=1)


def test_context_kwargs_marker_overrides(pytester: pytest.Pytester) -> None:
    pytester.makepyfile("""
        import pytest

        @pytest.mark.context_kwargs({})
        def test_override_context_kw(pw_context_kwargs) -> None:
            assert pw_context_kwargs == {}
    """)
    pytester.runpytest().assert_outcomes(passed=1)
